"""Tests for load_tags"""
from jobs.batch.load_opinions import apply_source_schema, select_for_gold_insert
from pyspark.sql.types import BooleanType, IntegerType, TimestampType
from pyspark.testing import assertDataFrameEqual, assertSchemaEqual


def test_apply_schema(spark):
    """Asserts schema for staging data"""
    df = spark.read.option("header", True).csv("./data/opinions.csv")
    actual_df = apply_source_schema(df, spark)
    assert actual_df.schema.fields[0].dataType == IntegerType()
    assert actual_df.schema.fields[1].dataType == IntegerType()
    assert actual_df.schema.fields[2].dataType == IntegerType()
    assert actual_df.schema.fields[3].dataType == BooleanType()
    assert actual_df.schema.fields[4].dataType == TimestampType()
    assert actual_df.schema.fields[5].dataType == TimestampType()


def test_gold_insert_select(spark):
    """Asserts that schema for gold insert selection"""
    df = spark.read.option("header", True).csv("./data/opinions.csv")
    df = apply_source_schema(df, spark)
    expected_df = df.select("opinion_id", "opinion")
    actual_df = select_for_gold_insert(df)
    assertSchemaEqual(actual_df.schema, expected_df.schema)
    assertDataFrameEqual(actual_df, expected_df)
