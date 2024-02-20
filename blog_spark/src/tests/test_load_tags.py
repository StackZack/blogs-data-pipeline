"""Tests for load_tags"""
from jobs.batch.load_tags import apply_source_schema
from pyspark.sql.types import IntegerType, StringType, TimestampType


def test_apply_schema(spark):
    """Asserts schema for staging data"""
    df = spark.read.option("header", True).csv("./data/tags.csv")
    actual_df = apply_source_schema(df, spark)
    assert actual_df.schema.fields[0].dataType == IntegerType()
    assert actual_df.schema.fields[1].dataType == StringType()
    assert actual_df.schema.fields[2].dataType == TimestampType()
    assert actual_df.schema.fields[3].dataType == TimestampType()
