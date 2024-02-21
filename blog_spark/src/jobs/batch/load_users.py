"""Job for loading gold.favorites"""
from jobs.batch.common import BatchSessionHelper
from jobs.batch.schema import staging_users
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame


def execute() -> None:
    """Job entry point"""
    # Instantiate session
    session_helper = BatchSessionHelper("load_users")

    # Select from source table
    df = session_helper.read_table_to_df("staging.stg_users")

    # Apply schema to df selection
    df = apply_source_schema(df, session_helper.spark)

    # Modify selection for insert
    df = select_for_gold_insert(df)

    # Insert df into target table
    session_helper.write_df_to_table(df, "gold.users")


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
            "CAST(user_id AS INT) AS user_id",
            "CAST(first_name AS STRING) AS first_name",
            "CAST(last_name AS STRING) AS last_name",
            "CAST(email AS STRING) AS email",
            "CAST(created_at AS TIMESTAMP) AS created_at",
            "CAST(updated_at AS TIMESTAMP) AS updated_at",
        ).collect(),
        staging_users,
    )


def select_for_gold_insert(df: DataFrame) -> DataFrame:
    """
    Selects necessary columns for gold insert

    :param df: Stage table data with schema applied
    :type df: DataFrame
    :return: Selection for gold insert
    :rtype: DataFrame
    """
    return df.select("user_id", "first_name", "last_name", "email")
