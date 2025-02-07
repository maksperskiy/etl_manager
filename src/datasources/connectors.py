import os
from pyspark.sql import SparkSession
from django.conf import settings


class DataSourceConnector:
    def __init__(self, data_source):
        self.data_source = data_source
        os.environ["PYSPARK_SUBMIT_ARGS"] = (
            "--packages "
            "com.amazonaws:aws-java-sdk-bundle:1.12.262,"
            "org.apache.hadoop:hadoop-aws:3.3.4,"
            # 'com.google.guava:guava:14.0.1,'
            # 'com.clickhouse:clickhouse-jdbc:0.4.6,'
            "org.postgresql:postgresql:42.7.0"
            " pyspark-shell"
        )
        self.spark = (
            SparkSession.builder.master(settings.SPARK_MASTER_URL)
            .appName(f"{data_source.name}-{data_source.id}")
            .getOrCreate()
        )

    def connect(self):
        source_type = self.data_source.source_type
        config = self.data_source.config

        if source_type == "POSTGRES":
            return self._connect_postgres(config)
        elif source_type == "MYSQL":
            return self._connect_mysql(config)
        elif source_type in ["FILE", "S3"]:
            return self._connect_s3(config)
        else:
            raise ValueError("Unsupported data source type")

    def _connect_postgres(self, config):
        jdbc_url = (
            f"jdbc:postgresql://{config['host']}:{config['port']}/{config['database']}"
        )
        properties = {
            "user": config["user"],
            "password": config["password"],
            "driver": "org.postgresql.Driver",
        }
        if "options" in config:
            properties.update(config["options"])
        if "query" in config:
            table = f"({config['query']}) as tmp"
        else:
            table = config["table"]
        return self.spark.read.jdbc(url=jdbc_url, table=table, properties=properties)

    def _connect_mysql(self, config):
        jdbc_url = f"jdbc:mysql://{config['host']}:{config.get('port', '3306')}/{config['database']}"

        properties = {
            "user": config["user"],
            "password": config["password"],
            "driver": "com.mysql.cj.jdbc.Driver",
            "useSSL": str(config.get("use_ssl", False)),
            "serverTimezone": config.get("timezone", "UTC"),
        }

        if "options" in config:
            properties.update(config["options"])

        if "query" in config:
            table = f"({config['query']}) as tmp"
        else:
            table = config["table"]

        return self.spark.read.jdbc(url=jdbc_url, table=table, properties=properties)

    def _connect_s3(self, config):
        if self.data_source.upload:
            s3_path = f"{self.data_source.upload.name}"
            config["path"] = s3_path  # Обновляем путь для чтения

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
