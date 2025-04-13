import os
from typing import Any, Dict, Optional

from django.conf import settings
from pyspark.sql import DataFrame, SparkSession

from datasources.models.datasource import DataSource


class MySQLConnector:
    """A connector for reading from and writing to MySQL databases using Spark."""

    MYSQL_DRIVER_PATH = "/opt/bitnami/spark/jars/mysql-connector-java-8.0.33.jar"
    DEFAULT_PORT = "3306"
    DEFAULT_TIMEZONE = "UTC"
    DEFAULT_SSL = False

    def __init__(
        self, session_builder: SparkSession.Builder, data_source: DataSource
    ) -> None:
        """Initialize the MySQL connector with Spark session builder and data source configuration.

        Args:
            session_builder: Builder for creating Spark sessions
            data_source: Configuration for the MySQL data source
        """
        self.data_source = data_source
        self.session_builder = self._configure_spark_session(session_builder)

    @classmethod
    def _configure_spark_session(
        cls, session_builder: SparkSession.Builder
    ) -> SparkSession.Builder:
        """Configure the Spark session with MySQL driver.

        Args:
            session_builder: Spark session builder to configure

        Returns:
            Configured Spark session builder
        """
        return session_builder.config("spark.jars", cls.MYSQL_DRIVER_PATH)

    def _get_connection_properties(self) -> Dict[str, str]:
        """Get the connection properties for MySQL JDBC connection.

        Returns:
            Dictionary of connection properties
        """
        config = self.data_source.config.copy()
        properties = {
            "user": config["user"],
            "password": config["password"],
            "driver": "com.mysql.cj.jdbc.Driver",
            "useSSL": str(config.get("use_ssl", self.DEFAULT_SSL)),
            "serverTimezone": config.get("timezone", self.DEFAULT_TIMEZONE),
        }

        if "options" in config:
            properties.update(config["options"])

        return properties

    def _get_jdbc_url(self) -> str:
        """Construct the JDBC URL for MySQL connection.

        Returns:
            JDBC URL string
        """
        config = self.data_source.config
        host = config["host"]
        port = config.get("port", self.DEFAULT_PORT)
        database = config["database"]
        return f"jdbc:mysql://{host}:{port}/{database}"

    def get_dataframe(self) -> DataFrame:
        """Read data from MySQL into a Spark DataFrame.

        Returns:
            Spark DataFrame containing the MySQL data
        """
        spark = self.session_builder.getOrCreate()
        config = self.data_source.config
        table = f"({config['query']}) as tmp" if "query" in config else config["table"]

        return spark.read.jdbc(
            url=self._get_jdbc_url(),
            table=table,
            properties=self._get_connection_properties(),
        )

    def write_dataframe(self, df: DataFrame, mode: str = "append") -> None:
        """Write a DataFrame to MySQL.

        Args:
            df: DataFrame to write to MySQL
            mode: Write mode ('append', 'overwrite', 'ignore', 'error')

        Raises:
            ValueError: If the table name is not specified in the configuration
        """
        if "table" not in self.data_source.config:
            raise ValueError("Table name must be specified for write operations")

        df.write.jdbc(
            url=self._get_jdbc_url(),
            table=self.data_source.config["table"],
            mode=mode,
            properties=self._get_connection_properties(),
        )
