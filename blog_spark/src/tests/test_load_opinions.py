"""Tests for load_opinions"""
from jobs.batch.load_opinions import (
    apply_source_schema,
    select_for_activity_insert,
    select_for_gold_insert,
)
from jobs.batch.schema import gold_blog_activity, staging_opinions
from pyspark.sql.types import BooleanType, IntegerType, StructField, StructType
from pyspark.testing import assertSchemaEqual


def test_apply_schema(spark):
    """Asserts schema for staging data"""
    df = spark.read.option("header", True).csv("./data/opinions.csv")
    actual_df = apply_source_schema(df, spark)
    assertSchemaEqual(actual_df.schema, staging_opinions)
    assert actual_df.count() == 100


def test_gold_insert_select(spark):
    """Asserts that schema for gold insert selection"""
    expected_schema = StructType(
        [
            StructField("opinion_id", IntegerType(), True),
            StructField("opinion", BooleanType(), True),
        ]
    )
    df = spark.read.option("header", True).csv("./data/opinions.csv")
    df = apply_source_schema(df, spark)
    actual_df = select_for_gold_insert(df)
    assertSchemaEqual(actual_df.schema, expected_schema)
    assert actual_df.count() == 100


def test_gold_activity_insert_select(spark):
    df = spark.read.option("header", True).csv("./data/opinions.csv")
    df = apply_source_schema(df, spark)
    actual_df = select_for_activity_insert(df, spark)
    assertSchemaEqual(actual_df.schema, gold_blog_activity)
    assert actual_df.count() == 100
