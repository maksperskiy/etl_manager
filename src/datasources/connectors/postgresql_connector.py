from typing import Any, Dict

from pyspark.sql import DataFrame, SparkSession

from datasources.models.datasource import DataSource


class PostgreSQLConnector:
    """A connector for reading from and writing to PostgreSQL databases using Spark.

    This class handles the configuration and execution of Spark operations
    to interact with PostgreSQL databases.
    """

    POSTGRESQL_JDBC_DRIVER = "org.postgresql.Driver"
    DEFAULT_JDBC_JAR_PATH = "/opt/bitnami/spark/jars/postgresql-42.7.5.jar"
    VALID_WRITE_MODES = {"overwrite", "append", "ignore", "error"}

    def __init__(self, session_builder: SparkSession.Builder, data_source: DataSource):
        """Initialize the PostgreSQL connector.

        Args:
            session_builder: SparkSession builder for creating Spark sessions
            data_source: DataSource configuration containing connection details
        """
        self.data_source = data_source
        self.session_builder = self._configure_spark_session(session_builder)

    @classmethod
    def _configure_spark_session(
        cls, session_builder: SparkSession.Builder
    ) -> SparkSession.Builder:
        """Configure the Spark session with PostgreSQL JDBC driver.

        Args:
            session_builder: SparkSession builder to configure

        Returns:
            Configured SparkSession builder
        """
        return session_builder.config("spark.jars", cls.DEFAULT_JDBC_JAR_PATH)

    def _get_connection_properties(self) -> Dict[str, str]:
        """Create connection properties dictionary from data source config.

        Returns:
            Dictionary of JDBC connection properties
        """
        config = self.data_source.config
        properties = {
            "user": config["user"],
            "password": config["password"],
            "driver": self.POSTGRESQL_JDBC_DRIVER,
        }

        if "options" in config:
            properties.update(config["options"])

        return properties

    def _get_jdbc_url(self) -> str:
        """Construct the JDBC URL from data source configuration.

        Returns:
            JDBC connection URL string
        """
        config = self.data_source.config
        return (
            f"jdbc:postgresql://{config['host']}:{config['port']}/{config['database']}"
        )

    def get_dataframe(self) -> DataFrame:
        """Read data from PostgreSQL into a Spark DataFrame.

        Returns:
            Spark DataFrame containing the queried data

        Raises:
            ValueError: If required configuration is missing
        """
        config = self.data_source.config

        if "query" not in config and "table" not in config:
            raise ValueError(
                "Either 'query' or 'table' must be specified in the data source config"
            )

        spark = self.session_builder.getOrCreate()
        table_or_query = (
            f"({config['query']}) as tmp" if "query" in config else config["table"]
        )

        return spark.read.jdbc(
            url=self._get_jdbc_url(),
            table=table_or_query,
            properties=self._get_connection_properties(),
        )

    def write_dataframe(self, df: DataFrame, mode: str = "overwrite") -> None:
        """Write a DataFrame to PostgreSQL.

        Args:
            df: Spark DataFrame to write
            mode: Write mode ('overwrite', 'append', 'ignore', 'error')

        Raises:
            ValueError: If table name is missing or write mode is invalid
        """
        if mode not in self.VALID_WRITE_MODES:
            raise ValueError(
                f"Invalid write mode '{mode}'. Must be one of {self.VALID_WRITE_MODES}"
            )

        config = self.data_source.config
        if "table" not in config:
            raise ValueError(
                "Target table name must be specified in the data source config for write operations"
            )

        df.write.jdbc(
            url=self._get_jdbc_url(),
            table=config["table"],
            mode=mode,
            properties=self._get_connection_properties(),
        )
