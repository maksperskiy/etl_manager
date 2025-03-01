import os

from django.conf import settings
from pyspark.sql import DataFrame, SparkSession

from datasources.models.datasource import DataSource


class PostgresqlConnector:
    def __init__(self, session_builder: SparkSession.Builder, data_source: DataSource):
        self.data_source = data_source
        self.session_builder: SparkSession.Builder = (
            self.set_sparksessionbuilder_config(session_builder)
        )

    @classmethod
    def set_sparksessionbuilder_config(cls, sparksessionbuilder: SparkSession.Builder):
        return sparksessionbuilder.config(
            "spark.jars.packages", "org.postgresql:postgresql:42.7.0"
        )

    def get_dataframe(self) -> DataFrame:
        spark = self.session_builder.getOrCreate()
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
        return spark.read.jdbc(url=jdbc_url, table=table, properties=properties)
