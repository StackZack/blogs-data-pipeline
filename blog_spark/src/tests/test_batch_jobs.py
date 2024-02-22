"""Tests for load_comments"""
import pytest
from jobs.batch import (
    load_blog_tags,
    load_blogs,
    load_comments,
    load_favorites,
    load_opinions,
    load_tags,
    load_users,
    schema,
)
from pyspark.testing import assertSchemaEqual

TEST_DATA_PATH = "./data"
BATCH_JOBS = {
    "load_blog_tags": ("blog_tags.csv", load_blog_tags.apply_source_schema, schema.staging_blog_tags),
    "load_blogs": ("blogs.csv", load_blogs.apply_source_schema, schema.staging_blogs),
    "load_comments": ("comments.csv", load_comments.apply_source_schema, schema.staging_comments),
    "load_favorites": ("favorites.csv", load_favorites.apply_source_schema, schema.staging_favorites),
    "load_opinions": ("opinions.csv", load_opinions.apply_source_schema, schema.staging_opinions),
    "load_tags": ("tags.csv", load_tags.apply_source_schema, schema.staging_tags),
    "load_users": ("users.csv", load_users.apply_source_schema, schema.staging_users),
}


@pytest.mark.parametrize("file_name, schema_function, expected_schema", BATCH_JOBS.values(), ids=BATCH_JOBS.keys())
def test_apply_schema(spark, file_name, schema_function, expected_schema):
    """Asserts schema for staging data"""
    df = spark.read.option("header", True).csv(f"{TEST_DATA_PATH}/{file_name}")
    actual_df = schema_function(df, spark)
    assertSchemaEqual(actual_df.schema, expected_schema)
