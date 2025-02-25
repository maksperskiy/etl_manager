import os

from django.conf import settings
from pyspark.sql import SparkSession

from .mysql_connector import MysqlConnector
from .postgresql_connector import PostgresqlConnector
from .s3_connector import S3Connector


class DataSourceConnectorFactory:
    def __init__(self, data_source):
        self.data_source = data_source
        self.spark_init = SparkSession.builder.master(
            settings.SPARK_MASTER_URL
        ).appName(f"{data_source.name}-{data_source.id}")

    def get_connector(self):
        source_type = self.data_source.source_type

        if source_type == "POSTGRES":
            return PostgresqlConnector(self.spark_init, self.data_source)
        elif source_type == "MYSQL":
            return MysqlConnector(self.spark_init, self.data_source)
        elif source_type in ["FILE", "S3"]:
            return S3Connector(self.spark_init, self.data_source)
        else:
            raise ValueError("Unsupported data source type")
