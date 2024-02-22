"""Job for loading staging.stg_tags"""
from jobs.batch.common import BatchSessionHelper
from jobs.batch.schema import staging_tags
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame


def execute() -> None:
    """Job entry point"""
    # Instantiate session
    session_helper = BatchSessionHelper("load_tags")

    # Select from source table
    df = session_helper.read_csv_to_df("/shared/data/tags.csv")

    # Apply schema to df selection
    df = apply_source_schema(df, session_helper.spark)

    # Insert df into target table
    session_helper.write_df_to_table(df, "staging.stg_tags")


def apply_source_schema(df: DataFrame, spark: SparkSession) -> DataFrame:
    """
    Applies a schema to the source data present in the staging table

    :param df: Stage table data
    :type df: DataFrame
    :param spark: Job session
    :type spark: SparkSession
    :return: Stage table with expected schema applied
    :rtype: DataFrame
    """
    return spark.createDataFrame(
        df.selectExpr(
            "CAST(tag_id AS INT) AS tag_id",
            "CAST(name AS STRING) AS name",
            "CAST(created_at AS TIMESTAMP) AS created_at",
            "CAST(updated_at AS TIMESTAMP) AS updated_at",
        ).collect(),
        staging_tags,
    )
