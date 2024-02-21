"""Job for loading gold.favorites"""
from jobs.batch.common import BatchSessionHelper
from jobs.batch.schema import gold_blog_activity, staging_comments
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import lit


def execute() -> None:
    """Job entry point"""
    # Instantiate session
    session_helper = BatchSessionHelper("load_comments")

    # Select from source table
    df = session_helper.read_table_to_df("staging.stg_comments")

    # Apply schema to df selection
    df = apply_source_schema(df, session_helper.spark)

    # Modify selection for insert
    gold_df = select_for_gold_insert(df)
    activity_df = select_for_activity_insert(df, session_helper.spark)

    # Insert df into target table
    session_helper.write_df_to_table(gold_df, "gold.comments")
    session_helper.write_df_to_table(activity_df, "gold.blog_activity")


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


def select_for_activity_insert(df: DataFrame, spark: SparkSession) -> DataFrame:
    """
    Selects necessary columns for blog activity insert

    :param df: Stage table data with schema applied
    :type df: DataFrame
    :return: Selection for blog activity insert
    :rtype: DataFrame
    """
    return spark.createDataFrame(
        df.select(
            "blog_id",
            "user_id",
            "comment_id",
            lit(None).alias("favorite_id"),
            lit(None).alias("opinion_id"),
        ).collect(),
        gold_blog_activity,
    )
