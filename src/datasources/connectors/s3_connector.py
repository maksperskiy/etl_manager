import os
from pyspark.sql import SparkSession, DataFrame
from django.conf import settings

from datasources.models.datasource import DataSource


class S3Connector:
    def __init__(self, spark_init: SparkSession.Builder, data_source: DataSource):
        self.data_source = data_source
        self.spark: SparkSession = spark_init.config(
            "spark.jars.packages",
            "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262",
        ).getOrCreate()

    def connect(self) -> DataFrame:
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
        self.spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", access_key)
        self.spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", secret_key)
        self.spark._jsc.hadoopConfiguration().set(
            "com.amazonaws.services.s3.enableV4", "true"
        )
        self.spark._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
        self.spark._jsc.hadoopConfiguration().set("fs.s3a.endpoint", endpoint_url)
        self.spark._jsc.hadoopConfiguration().set("fs.s3a.endpoint.region", region_name)
        self.spark._jsc.hadoopConfiguration().set(
            "fs.s3a.aws.credentials.provider",
            "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
        )

        # Чтение данных в зависимости от типа
        if file_type == "csv":
            return self.spark.read.csv(s3_path, **config.get("options", {}))
        elif file_type == "json":
            return self.spark.read.json(s3_path, **config.get("options", {}))
        elif file_type == "parquet":
            return self.spark.read.parquet(s3_path)
        elif file_type in ["xlsx", "xls"]:
            return (
                self.spark.read.format("com.crealytics.spark.excel")
                .option("header", "true")
                .load(s3_path)
            )
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
