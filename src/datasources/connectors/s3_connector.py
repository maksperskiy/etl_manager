import os
from typing import Any, Dict, Optional

from django.conf import settings
from pyspark.sql import DataFrame, SparkSession

from datasources.models.datasource import DataSource


class S3ConfigurationError(ValueError):
    """Exception raised for errors in S3 configuration."""

    pass


class UnsupportedFileTypeError(ValueError):
    """Exception raised for unsupported file types."""

    pass


class S3Connector:
    """Handles data transfer between S3-compatible storage and Spark DataFrames."""

    # Configuration constants
    _SPARK_JARS = [
        "/opt/bitnami/spark/jars/hadoop-aws-3.3.4.jar",
        "/opt/bitnami/spark/jars/aws-java-sdk-bundle-1.12.262.jar",
        "/opt/bitnami/spark/jars/spark-excel_2.12-0.13.1.jar",
    ]
    _HADOOP_CONFIG = {
        "access_key": "fs.s3a.access.key",
        "secret_key": "fs.s3a.secret.key",
        "enable_v4": "com.amazonaws.services.s3.enableV4",
        "path_style": "fs.s3a.path.style.access",
        "endpoint": "fs.s3a.endpoint",
        "region": "fs.s3a.endpoint.region",
        "credentials_provider": "fs.s3a.aws.credentials.provider",
    }
    _CREDENTIALS_PROVIDER = "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider"
    _SUPPORTED_READ_TYPES = {"csv", "json", "parquet", "xlsx", "xls"}
    _SUPPORTED_WRITE_TYPES = {"csv", "json", "parquet", "xlsx", "xls"}

    def __init__(self, session_builder: SparkSession.Builder, data_source: DataSource):
        self.data_source = data_source
        self.spark_session = self._configure_spark(session_builder)

    def _configure_spark(self, builder: SparkSession.Builder) -> SparkSession.Builder:
        """Configures Spark session with required dependencies."""
        return builder.config("spark.jars", ",".join(self._SPARK_JARS))

    def _get_storage_config(self) -> Dict[str, str]:
        """Retrieves and validates storage configuration."""
        if self.data_source.upload:
            return self._get_upload_config()
        return self._get_external_config()

    def _get_upload_config(self) -> Dict[str, str]:
        """Gets configuration for uploaded files."""
        try:
            options = settings.STORAGES["default"]["OPTIONS"]
            return {
                "bucket": options["bucket_name"],
                "access_key": options["access_key"],
                "secret_key": options["secret_key"],
                "endpoint": options["endpoint_url"],
                "region": options["region_name"],
                "path": self.data_source.upload.name,
            }
        except KeyError as e:
            raise S3ConfigurationError(f"Missing storage configuration: {e}") from e

    def _get_external_config(self) -> Dict[str, str]:
        """Gets configuration for external S3 storage."""
        config = self.data_source.config
        required_keys = {
            "bucket",
            "access_key",
            "secret_key",
            "endpoint",
            "region",
            "path",
        }
        missing = required_keys - config.keys()
        if missing:
            raise S3ConfigurationError(
                f"Missing configuration keys: {', '.join(missing)}"
            )
        return {k: config[k] for k in required_keys}

    def _configure_hadoop(self, spark: SparkSession, config: Dict[str, str]) -> None:
        """Applies S3-compatible storage configuration to Hadoop."""
        hadoop = spark._jsc.hadoopConfiguration()
        hadoop.set(self._HADOOP_CONFIG["access_key"], config["access_key"])
        hadoop.set(self._HADOOP_CONFIG["secret_key"], config["secret_key"])
        hadoop.set(self._HADOOP_CONFIG["enable_v4"], "true")
        hadoop.set(self._HADOOP_CONFIG["path_style"], "true")
        hadoop.set(self._HADOOP_CONFIG["endpoint"], config["endpoint"])
        hadoop.set(self._HADOOP_CONFIG["region"], config["region"])
        hadoop.set(
            self._HADOOP_CONFIG["credentials_provider"], self._CREDENTIALS_PROVIDER
        )

    def _get_file_type(self, path: str) -> str:
        """Determines file type from path and configuration."""
        file_type = (
            self.data_source.config.get("file_type") or path.split(".")[-1].lower()
        )
        if not file_type or "." not in path:
            raise ValueError("Could not determine file type from path or configuration")
        return file_type

    def _get_s3_path(self, bucket: str, path: str) -> str:
        """Constructs fully qualified S3 path."""
        return f"s3a://{bucket}/{path}"

    def get_dataframe(self) -> DataFrame:
        """Reads data from S3-compatible storage into a DataFrame."""
        config = self._get_storage_config()
        spark = self.spark_session.getOrCreate()
        self._configure_hadoop(spark, config)

        file_type = self._get_file_type(config["path"])
        if file_type not in self._SUPPORTED_READ_TYPES:
            raise UnsupportedFileTypeError(
                f"Reading {file_type} files is not supported"
            )

        s3_path = self._get_s3_path(config["bucket"], config["path"])
        options = self.data_source.config.get("options", {})

        return self._read_data(spark, file_type, s3_path, options)

    def _read_data(
        self, spark: SparkSession, file_type: str, path: str, options: Dict
    ) -> DataFrame:
        """Dispatches to appropriate reader based on file type."""
        readers = {
            "csv": lambda: spark.read.csv(path, **options),
            "json": lambda: spark.read.json(path, **options),
            "parquet": lambda: spark.read.parquet(path),
            "xlsx": lambda: spark.read.format("com.crealytics.spark.excel")
            .option("header", "true")
            .load(path),
            "xls": lambda: spark.read.format("com.crealytics.spark.excel")
            .option("header", "true")
            .load(path),
        }
        return readers[file_type]()

    def write_dataframe(self, df: DataFrame) -> None:
        """Writes DataFrame to S3-compatible storage."""
        config = self._get_storage_config()
        spark = self.spark_session.getOrCreate()
        self._configure_hadoop(spark, config)

        file_type = self._get_file_type(config["path"])
        if file_type not in self._SUPPORTED_WRITE_TYPES:
            raise UnsupportedFileTypeError(
                f"Writing {file_type} files is not supported"
            )

        s3_path = self._get_s3_path(config["bucket"], config["path"])
        options = self.data_source.config.get("options", {})

        self._write_data(df, file_type, s3_path, options)

    def _write_data(
        self, df: DataFrame, file_type: str, path: str, options: Dict
    ) -> None:
        """Dispatches to appropriate writer based on file type."""
        writers = {
            "csv": lambda: df.write.options(**options).csv(path),
            "json": lambda: df.write.options(**options).json(path),
            "parquet": lambda: df.write.options(**options).parquet(path),
            "xlsx": lambda: df.write.format("com.crealytics.spark.excel")
            .option("header", "true")
            .options(**options)
            .save(path),
            "xls": lambda: df.write.format("com.crealytics.spark.excel")
            .option("header", "true")
            .options(**options)
            .save(path),
        }
        writers[file_type]()
