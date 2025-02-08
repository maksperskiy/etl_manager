import os
from pyspark.sql import SparkSession, DataFrame
from django.conf import settings

from datasources.models.datasource import DataSource


class PostgresqlConnector:
    def __init__(self, spark_init: SparkSession.Builder, data_source: DataSource):
        self.data_source = data_source
        self.spark: SparkSession = spark_init.config(
            "spark.jars.packages", "org.postgresql:postgresql:42.7.0"
        ).getOrCreate()

    def connect(self) -> DataFrame:
        config = self.data_source.config.copy()
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
