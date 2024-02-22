"""Schemas for pyspark jobs"""
from pyspark.sql.types import (
    BooleanType,
    DateType,
    IntegerType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

staging_tags = StructType(
    [
        StructField("tag_id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("created_at", TimestampType(), True),
        StructField("updated_at", TimestampType(), True),
    ]
)

staging_opinions = StructType(
    [
        StructField("opinion_id", IntegerType(), True),
        StructField("blog_id", IntegerType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("opinion", BooleanType(), True),
        StructField("created_at", TimestampType(), True),
        StructField("updated_at", TimestampType(), True),
    ]
)

staging_favorites = StructType(
    [
        StructField("favorite_id", IntegerType(), True),
        StructField("blog_id", IntegerType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("favorite_date", DateType(), True),
        StructField("created_at", TimestampType(), True),
        StructField("updated_at", TimestampType(), True),
    ]
)

staging_comments = StructType(
    [
        StructField("comment_id", IntegerType(), True),
        StructField("blog_id", IntegerType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("content", StringType(), True),
        StructField("created_at", TimestampType(), True),
        StructField("updated_at", TimestampType(), True),
    ]
)

staging_users = StructType(
    [
        StructField("user_id", IntegerType(), True),
        StructField("first_name", StringType(), True),
        StructField("last_name", StringType(), True),
        StructField("email", StringType(), True),
        StructField("created_at", TimestampType(), True),
        StructField("updated_at", TimestampType(), True),
    ]
)

staging_blogs = StructType(
    [
        StructField("blog_id", IntegerType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("title", StringType(), True),
        StructField("content", StringType(), True),
        StructField("created_at", TimestampType(), True),
        StructField("updated_at", TimestampType(), True),
    ]
)

staging_blog_tags = StructType(
    [
        StructField("blog_id", IntegerType(), True),
        StructField("tag_id", IntegerType(), True),
    ]
)
