import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pyspark.sql import SparkSession, Window, DataFrame
from pyspark.sql import functions as F

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Transformation(ABC):
    """Base class for all transformation operations."""

    @abstractmethod
    def apply(self, df: DataFrame, config: Dict[str, Any]) -> DataFrame:
        """Apply the transformation to the DataFrame."""
        pass


class FilterTransformation(Transformation):
    """Apply a filter transformation."""

    def apply(self, df: DataFrame, config: Dict[str, Any]) -> DataFrame:
        condition = config.get("condition")
        if not condition:
            raise ValueError("Filter condition not provided.")
        return df.filter(condition)


class SelectTransformation(Transformation):
    """Apply a select transformation."""

    def apply(self, df: DataFrame, config: Dict[str, Any]) -> DataFrame:
        columns = config.get("columns")
        if not columns:
            raise ValueError("Columns to select not provided.")
        return df.select(*columns)


class JoinTransformation(Transformation):
    """Apply a join transformation."""

    def apply(
        self, df: DataFrame, config: Dict[str, Any], dataframes: Dict[str, DataFrame]
    ) -> DataFrame:
        df2_name = config.get("df2")
        if df2_name not in dataframes:
            raise ValueError(f"DataFrame '{df2_name}' not found in input_dataframes.")
        df2 = dataframes[df2_name]
        on_column = config.get("on")
        how = config.get("how", "inner")

        # Resolve ambiguous column names by renaming conflicting columns
        conflicting_columns = set(df.columns).intersection(set(df2.columns)) - {
            on_column
        }
        for col in conflicting_columns:
            df2 = df2.withColumnRenamed(col, f"{col}_df2")

        return df.join(df2, on=on_column, how=how)


class GroupByTransformation(Transformation):
    """Apply a groupby transformation."""

    def apply(self, df: DataFrame, config: Dict[str, Any]) -> DataFrame:
        groupby_columns = config.get("groupby_columns")
        aggregations = config.get("aggregations")
        if not groupby_columns or not aggregations:
            raise ValueError("Groupby columns or aggregations not provided.")

        agg_exprs = []
        for agg in aggregations:
            column = agg.get("column")
            operation = agg.get("operation")
            alias = agg.get("alias")
            if not column or not operation or not alias:
                raise ValueError(
                    "Aggregation column, operation, or alias not provided."
                )
            agg_exprs.append(F.expr(f"{operation}({column}) as {alias}"))

        return df.groupBy(*groupby_columns).agg(*agg_exprs)


class WindowTransformation(Transformation):
    """Apply a window transformation."""

    def apply(self, df: DataFrame, config: Dict[str, Any]) -> DataFrame:
        partition_by = config.get("partition_by")
        order_by = config.get("order_by")
        window_functions = config.get("window_functions")
        if not partition_by or not order_by or not window_functions:
            raise ValueError(
                "Partition by, order by, or window functions not provided."
            )

        window_spec = Window.partitionBy(*partition_by).orderBy(*order_by)

        for wf in window_functions:
            column = wf.get("column")
            operation = wf.get("operation")
            alias = wf.get("alias")
            if not column or not operation or not alias:
                raise ValueError(
                    "Window function column, operation, or alias not provided."
                )

            if operation == "row_number":
                df = df.withColumn(alias, F.row_number().over(window_spec))
            elif operation == "rank":
                df = df.withColumn(alias, F.rank().over(window_spec))
            elif operation == "dense_rank":
                df = df.withColumn(alias, F.dense_rank().over(window_spec))
            elif operation == "lead":
                offset = wf.get("offset", 1)
                df = df.withColumn(alias, F.lead(column, offset).over(window_spec))
            elif operation == "lag":
                offset = wf.get("offset", 1)
                df = df.withColumn(alias, F.lag(column, offset).over(window_spec))
            elif operation == "sum":
                df = df.withColumn(alias, F.sum(column).over(window_spec))
            elif operation == "avg":
                df = df.withColumn(alias, F.avg(column).over(window_spec))
            else:
                raise ValueError(f"Unsupported window function: {operation}")

        return df


class DataFrameTransformer:
    """Responsible for applying transformations to DataFrames based on the config."""

    def __init__(self, dataframes: Dict[str, DataFrame]):
        self.dataframes = dataframes
        self.transformations = {
            "filter": FilterTransformation(),
            "select": SelectTransformation(),
            "join": JoinTransformation(),
            "groupby": GroupByTransformation(),
            "window": WindowTransformation(),
        }

    def transform(
        self, transform_configs: List[Dict[str, Any]]
    ) -> Dict[str, DataFrame]:
        """Apply transformations defined in the JSON config."""
        if not self.dataframes:
            raise ValueError(
                "No DataFrames provided. Ensure input_dataframes is populated."
            )

        for transform in transform_configs:
            transform_type = transform.get("type")
            df_name = transform.get("df")
            alias = transform.get("alias")

            if df_name not in self.dataframes:
                raise ValueError(
                    f"DataFrame '{df_name}' not found in input_dataframes."
                )

            df = self.dataframes[df_name]

            if transform_type not in self.transformations:
                raise ValueError(f"Unsupported transformation: {transform_type}")

            transformation = self.transformations[transform_type]
            if transform_type == "join":
                df = transformation.apply(df, transform, self.dataframes)
            else:
                df = transformation.apply(df, transform)
            
            if alias:
                self.dataframes[alias] = df
            else:
                raise ValueError("Alias not provided for the transformed DataFrame.")

        return self.dataframes


class ETLPipeline:
    """Orchestrates the ETL pipeline."""

    def __init__(self, config: dict, input_dataframes: Dict[str, DataFrame], spark_session_builder: SparkSession.Builder = None, result_df_name: str = None):
        self.config = config
        self.spark = (spark_session_builder or SparkSession.builder.appName("ETLPipeline")).getOrCreate()
        self.dataframes = input_dataframes
        self.transformer = DataFrameTransformer(self.dataframes)
        self.result_df_name = result_df_name or "transformed_df"

    def run(self) -> Optional[DataFrame]:
        """Execute the ETL pipeline."""
        try:
            transform_configs = self.config
            self.dataframes = self.transformer.transform(transform_configs)
            logger.info("ETL transformations executed successfully.")
            print(self.dataframes.keys())
            return self.dataframes[self.result_df_name]
        except Exception as e:
            logger.error(f"ETL pipeline failed: {e}")
            raise
        finally:
            pass
            # self.spark.stop()


# Example Usage
if __name__ == "__main__":
    # Example input DataFrames
    spark = SparkSession.builder.appName("Example").getOrCreate()
    input_data = spark.createDataFrame(
        [
            (1, "Alice", 25, 50000, "HR"),
            (2, "Bob", 35, 60000, "Engineering"),
            (3, "Charlie", 40, 70000, "Engineering"),
            (4, "David", 30, 55000, "HR"),
        ],
        ["id", "name", "age", "salary", "department"],
    )

    # Dictionary of existing DataFrames
    input_dataframes = {"input_data": input_data}

    # Parse and run the ETL pipeline
    etl_pipeline = ETLPipeline(
        {
            "transform": [
                {
                    "type": "groupby",
                    "df": "input_data",
                    "groupby_columns": ["department"],
                    "aggregations": [
                        {"column": "salary", "operation": "avg", "alias": "avg_salary"},
                        {"column": "age", "operation": "max", "alias": "max_age"},
                    ],
                    "alias": "grouped_data",
                },
                {
                    "type": "window",
                    "df": "grouped_data",
                    "partition_by": ["department"],
                    "order_by": ["avg_salary"],
                    "window_functions": [
                        {
                            "column": "avg_salary",
                            "operation": "row_number",
                            "alias": "salary_rank",
                        },
                        {
                            "column": "avg_salary",
                            "operation": "lead",
                            "alias": "next_avg_salary",
                            "offset": 1,
                        },
                        {
                            "column": "avg_salary",
                            "operation": "lag",
                            "alias": "prev_avg_salary",
                            "offset": 1,
                        },
                        {
                            "column": "avg_salary",
                            "operation": "sum",
                            "alias": "cumulative_salary",
                        },
                    ],
                    "alias": "ranked_data",
                },
                {
                    "type": "select",
                    "df": "ranked_data",
                    "columns": ["department", "max_age", "avg_salary"],
                    "alias": "selected_data"
                },
            ]
        },
        input_dataframes,
    )
    final_df = etl_pipeline.run()

    if final_df:
        final_df.show()
