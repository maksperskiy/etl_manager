import os
from pyspark.sql import SparkSession, DataFrame
from django.conf import settings

from datasources.models.datasource import DataSource


class MysqlConnector:
    def __init__(self, spark_init: SparkSession.Builder, data_source: DataSource):
        self.data_source = data_source
        self.spark: SparkSession = spark_init.config(
            "spark.jars.packages", "mysql:mysql-connector-java:8.0.11"
        ).getOrCreate()

    def connect(self) -> DataFrame:
        config = self.data_source.config.copy()
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
