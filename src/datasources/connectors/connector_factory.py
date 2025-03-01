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

    def get_connector(self, session_builder=None):
        if not session_builder:
            session_builder = self.spark_init
        source_type = self.data_source.source_type

        if source_type == "POSTGRES":
            return PostgresqlConnector(session_builder, self.data_source)
        elif source_type == "MYSQL":
            return MysqlConnector(session_builder, self.data_source)
        elif source_type in ["FILE", "S3"]:
            return S3Connector(session_builder, self.data_source)
        else:
            raise ValueError("Unsupported data source type")
