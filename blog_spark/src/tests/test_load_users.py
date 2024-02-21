"""Tests for load_users"""
from jobs.batch.load_users import apply_source_schema, select_for_gold_insert
from jobs.batch.schema import staging_users
from pyspark.sql.types import IntegerType, StringType, StructField, StructType
from pyspark.testing import assertSchemaEqual


def test_apply_schema(spark):
    """Asserts schema for staging data"""
    df = spark.read.option("header", True).csv("./data/users.csv")
    actual_df = apply_source_schema(df, spark)
    assertSchemaEqual(actual_df.schema, staging_users)
    assert actual_df.count() == 100


def test_gold_insert_select(spark):
    """Asserts that schema for gold insert selection"""
    expected_schema = StructType(
        [
            StructField("user_id", IntegerType(), True),
            StructField("first_name", StringType(), True),
            StructField("last_name", StringType(), True),
            StructField("email", StringType(), True),
        ]
    )
    df = spark.read.option("header", True).csv("./data/users.csv")
    df = apply_source_schema(df, spark)
    actual_df = select_for_gold_insert(df)
    assertSchemaEqual(actual_df.schema, expected_schema)
    assert actual_df.count() == 100
