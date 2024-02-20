"""Schemas for pyspark jobs"""
from pyspark.sql.types import (
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
