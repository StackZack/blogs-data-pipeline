"""Job for loading staging.stg_favorites"""
from jobs.batch.common import BatchSessionHelper
from jobs.batch.schema import staging_favorites
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame


def execute() -> None:
    """Job entry point"""
    # Instantiate session
    session_helper = BatchSessionHelper("load_favorites")

    # Select from source file
    df = session_helper.read_csv_to_df("/shared/data/favorites.csv")

    # Apply schema to df selection
    df = apply_source_schema(df, session_helper.spark)

    # Insert df into target table
    session_helper.write_df_to_table(df, "staging.stg_favorites")


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
            "CAST(favorite_id AS INT) AS favorite_id",
            "CAST(blog_id AS INT) AS blog_id",
            "CAST(user_id AS INT) AS user_id",
            "CAST(favorite_date AS DATE) AS favorite_date",
            "CAST(created_at AS TIMESTAMP) AS created_at",
            "CAST(updated_at AS TIMESTAMP) AS updated_at",
        ).collect(),
        staging_favorites,
    )
