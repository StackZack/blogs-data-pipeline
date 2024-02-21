"""Tests for load_comments"""
from jobs.batch.load_comments import (
    apply_source_schema,
    select_for_activity_insert,
    select_for_gold_insert,
)
from jobs.batch.schema import gold_blog_activity, staging_comments
from pyspark.sql.types import IntegerType, StringType, StructField, StructType
from pyspark.testing import assertSchemaEqual


def test_apply_schema(spark):
    """Asserts schema for staging data"""
    df = spark.read.option("header", True).csv("./data/comments.csv")
    actual_df = apply_source_schema(df, spark)
    assertSchemaEqual(actual_df.schema, staging_comments)


def test_gold_insert_select(spark):
    """Asserts that schema for gold insert selection"""
    expected_schema = StructType(
        [
            StructField("comment_id", IntegerType(), True),
            StructField("content", StringType(), True),
        ]
    )
    df = spark.read.option("header", True).csv("./data/comments.csv")
    df = apply_source_schema(df, spark)
    actual_df = select_for_gold_insert(df)
    assertSchemaEqual(actual_df.schema, expected_schema)
    assert actual_df.count() == 100


def test_gold_activity_insert_select(spark):
    df = spark.read.option("header", True).csv("./data/comments.csv")
    df = apply_source_schema(df, spark)
    actual_df = select_for_activity_insert(df, spark)
    assertSchemaEqual(actual_df.schema, gold_blog_activity)
    assert actual_df.count() == 100
