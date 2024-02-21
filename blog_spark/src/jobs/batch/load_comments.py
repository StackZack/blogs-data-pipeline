"""Job for loading gold.favorites"""
from jobs.batch.common import BatchSessionHelper
from jobs.batch.schema import staging_comments
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame


def execute() -> None:
    """Job entry point"""
    # Instantiate session
    session_helper = BatchSessionHelper("load_comments")

    # Select from source table
    df = session_helper.read_table_to_df("staging.stg_comments")

    # Apply schema to df selection
    df = apply_source_schema(df, session_helper.spark)

    # Modify selection for insert
    df = select_for_gold_insert(df)

    # Insert df into target table
    session_helper.write_df_to_table(df, "gold.comments")


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
            "CAST(comment_id AS INT) AS comment_id",
            "CAST(blog_id AS INT) AS blog_id",
            "CAST(user_id AS INT) AS user_id",
            "CAST(content AS STRING) AS content",
            "CAST(created_at AS TIMESTAMP) AS created_at",
            "CAST(updated_at AS TIMESTAMP) AS updated_at",
        ).collect(),
        staging_comments,
    )


def select_for_gold_insert(df: DataFrame) -> DataFrame:
    """
    Selects necessary columns for gold insert

    :param df: Stage table data with schema applied
    :type df: DataFrame
    :return: Selection for gold insert
    :rtype: DataFrame
    """
    return df.select("comment_id", "content")
