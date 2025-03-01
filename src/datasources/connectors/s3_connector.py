import os

from django.conf import settings
from pyspark.sql import DataFrame, SparkSession

from datasources.models.datasource import DataSource


class S3Connector:
    def __init__(self, session_builder: SparkSession.Builder, data_source: DataSource):
        self.data_source = data_source
        self.session_builder: SparkSession.Builder = (
            self.set_sparksessionbuilder_config(session_builder)
        )

    @classmethod
    def set_sparksessionbuilder_config(cls, sparksessionbuilder: SparkSession.Builder):
        return sparksessionbuilder.config(
            "spark.jars.packages",
            "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262,"
            "com.crealytics:spark-excel_2.12:0.13.5",
        )

    def get_dataframe(self) -> DataFrame:
        spark = self.session_builder.getOrCreate()
        config = self.data_source.config.copy()
        if self.data_source.upload:
            s3_path = f"{self.data_source.upload.name}"
            config["path"] = s3_path

        # Определение формата файла
        path = config["path"]
        file_ext = path.split(".")[-1].lower() if "." in path else None
        file_type = config.get("file_type") or file_ext

        if self.data_source.upload:

            storage_config = settings.STORAGES["default"]["OPTIONS"]
            bucket = storage_config["bucket_name"]
            access_key = storage_config["access_key"]
            secret_key = storage_config["secret_key"]
            endpoint_url = storage_config["endpoint_url"]
            region_name = storage_config["region_name"]
        else:
            bucket = config["bucket"]
            access_key = config["access_key"]
            secret_key = config["secret_key"]
            endpoint_url = config["endpoint_url"]
            region_name = config["region_name"]

        # Формирование пути S3
        s3_path = f"s3a://{bucket}/{path}"

        # Настройка Spark для работы с MinIO
        spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", access_key)
        spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", secret_key)
        spark._jsc.hadoopConfiguration().set(
            "com.amazonaws.services.s3.enableV4", "true"
        )
        spark._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
        spark._jsc.hadoopConfiguration().set("fs.s3a.endpoint", endpoint_url)
        spark._jsc.hadoopConfiguration().set("fs.s3a.endpoint.region", region_name)
        spark._jsc.hadoopConfiguration().set(
            "fs.s3a.aws.credentials.provider",
            "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
        )

        # Чтение данных в зависимости от типа
        if file_type == "csv":
            return spark.read.csv(s3_path, **config.get("options", {}))
        elif file_type == "json":
            return spark.read.json(s3_path, **config.get("options", {}))
        elif file_type == "parquet":
            return spark.read.parquet(s3_path)
        elif file_type in ["xlsx", "xls"]:
            return (
                spark.read.format("com.crealytics.spark.excel")
                .option("header", "true")
                .load(s3_path)
            )
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
