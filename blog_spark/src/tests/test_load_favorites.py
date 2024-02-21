"""Tests for load_favorites"""
from jobs.batch.load_favorites import (
    apply_source_schema,
    select_for_activity_insert,
    select_for_gold_insert,
)
from jobs.batch.schema import gold_blog_activity, staging_favorites
from pyspark.sql.types import DateType, IntegerType, StructField, StructType
from pyspark.testing import assertSchemaEqual


def test_apply_schema(spark):
    """Asserts schema for staging data"""
    df = spark.read.option("header", True).csv("./data/favorites.csv")
    actual_df = apply_source_schema(df, spark)
    assertSchemaEqual(actual_df.schema, staging_favorites)
    assert actual_df.count() == 100


def test_gold_insert_select(spark):
    """Asserts that schema for gold insert selection"""
    expected_schema = StructType(
        [
            StructField("favorite_id", IntegerType(), True),
            StructField("favorite_date", DateType(), True),
        ]
    )
    df = spark.read.option("header", True).csv("./data/favorites.csv")
    df = apply_source_schema(df, spark)
    actual_df = select_for_gold_insert(df)
    assertSchemaEqual(actual_df.schema, expected_schema)
    assert actual_df.count() == 100


def test_gold_activity_insert_select(spark):
    df = spark.read.option("header", True).csv("./data/favorites.csv")
    df = apply_source_schema(df, spark)
    actual_df = select_for_activity_insert(df, spark)
    assertSchemaEqual(actual_df.schema, gold_blog_activity)
    assert actual_df.count() == 100
