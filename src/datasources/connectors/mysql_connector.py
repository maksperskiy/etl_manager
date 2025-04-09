import os

from django.conf import settings
from pyspark.sql import DataFrame, SparkSession

from datasources.models.datasource import DataSource


class MysqlConnector:
    def __init__(self, session_builder: SparkSession.Builder, data_source: DataSource):
        self.data_source = data_source
        self.session_builder: SparkSession.Builder = (
            self.set_sparksessionbuilder_config(session_builder)
        )

    @classmethod
    def set_sparksessionbuilder_config(cls, sparksessionbuilder: SparkSession.Builder):
        return sparksessionbuilder.config(
            "spark.jars", "/opt/bitnami/spark/jars/mysql-connector-java-8.0.33.jar"
        )

    def get_dataframe(self) -> DataFrame:
        spark = self.session_builder.getOrCreate()
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

        return spark.read.jdbc(url=jdbc_url, table=table, properties=properties)
