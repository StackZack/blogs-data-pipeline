"""Job for loading gold.opinions"""
from jobs.batch.common import BatchSessionHelper
from jobs.batch.schema import gold_blog_activity, staging_opinions
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import lit


def execute() -> None:
    """Job entry point"""
    # Instantiate session
    session_helper = BatchSessionHelper("load_opinions")

    # Select from source table
    df = session_helper.read_table_to_df("staging.stg_opinions")

    # Apply schema to df selection
    df = apply_source_schema(df, session_helper.spark)

    # Modify selection for inserts
    gold_df = select_for_gold_insert(df)
    activity_df = select_for_activity_insert(df, session_helper.spark)

    # Insert df into target table
    session_helper.write_df_to_table(gold_df, "gold.opinions")
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
            "CAST(opinion_id AS INT) AS opinion_id",
            "CAST(blog_id AS INT) AS blog_id",
            "CAST(user_id AS INT) AS user_id",
            "CAST(opinion AS BOOLEAN) AS opinion",
            "CAST(created_at AS TIMESTAMP) AS created_at",
            "CAST(updated_at AS TIMESTAMP) AS updated_at",
        ).collect(),
        staging_opinions,
    )


def select_for_gold_insert(df: DataFrame) -> DataFrame:
    """
    Selects necessary columns for gold insert

    :param df: Stage table data with schema applied
    :type df: DataFrame
    :return: Selection for gold insert
    :rtype: DataFrame
    """
    return df.select("opinion_id", "opinion")


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
            lit(None).alias("comment_id"),
            lit(None).alias("favorite_id"),
            "opinion_id",
        ).collect(),
        gold_blog_activity,
    )
