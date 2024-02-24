from jobs.batch.load_blog_stage_tables import mask_users_df
from jobs.batch.schema import staging_users


def check_masked_string(string):
    return all(char == "*" for char in string)


def test_mask_users_data(spark):
    """Asserts that users data is correctly masked"""
    df = spark.read.option("header", True).csv("./data/users.csv", schema=staging_users)
    actual_df = mask_users_df(df)
    actual_rows = actual_df.collect()
    for row in actual_rows:
        assert check_masked_string(row["first_name"][1:])
        assert check_masked_string(row["last_name"][1:])
        assert check_masked_string(row["email"].split("@")[1:-1])
