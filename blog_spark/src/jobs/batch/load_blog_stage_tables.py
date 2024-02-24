"""Job for loading staging tables"""
from jobs.batch.common import BatchSessionHelper
from jobs.batch.schema import (
    staging_blog_tags,
    staging_blogs,
    staging_comments,
    staging_favorites,
    staging_opinions,
    staging_tags,
    staging_users,
)
from pyspark.sql import DataFrame
from pyspark.sql.functions import regexp_replace


def execute() -> None:
    """Job entry point"""
    # Instantiate session
    session_helper = BatchSessionHelper("load_blog_tags")
    csv_path = "/shared/data"
    spark = session_helper.spark

    # Select from source table
    blog_tags_df = spark.read.option("header", True).csv(f"{csv_path}/blog_tags.csv", schema=staging_blog_tags)
    blogs_df = spark.read.option("header", True).csv(f"{csv_path}/blogs.csv", schema=staging_blogs)
    users_df = spark.read.option("header", True).csv(f"{csv_path}/users.csv", schema=staging_users)
    users_df = mask_users_df(users_df)
    tags_df = spark.read.option("header", True).csv(f"{csv_path}/tags.csv", schema=staging_tags)
    opinions_df = spark.read.option("header", True).csv(f"{csv_path}/opinions.csv", schema=staging_opinions)
    favorites_df = spark.read.option("header", True).csv(f"{csv_path}/favorites.csv", schema=staging_favorites)
    comments_df = spark.read.option("header", True).csv(f"{csv_path}/comments.csv", schema=staging_comments)

    # Insert df into target table
    session_helper.write_df_to_table(blog_tags_df, "staging.stg_blog_tags")
    session_helper.write_df_to_table(blogs_df, "staging.stg_blogs")
    session_helper.write_df_to_table(users_df, "staging.stg_users")
    session_helper.write_df_to_table(tags_df, "staging.stg_tags")
    session_helper.write_df_to_table(opinions_df, "staging.stg_opinions")
    session_helper.write_df_to_table(favorites_df, "staging.stg_favorites")
    session_helper.write_df_to_table(comments_df, "staging.stg_comments")


def mask_users_df(df: DataFrame) -> DataFrame:
    """
    Masks PII values in user data

    :param df: Users data to be masked
    :type df: DataFrame
    :return: Masked user data
    :rtype: DataFrame
    """
    return (
        df.withColumn("first_name", regexp_replace("first_name", "(?<!^).", "*"))
        .withColumn("last_name", regexp_replace("last_name", "(?<!^).", "*"))
        .withColumn("email", regexp_replace("email", "(?<!^).(?=.+@)", "*"))
    )
