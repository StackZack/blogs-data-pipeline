"""Helper methods and classes for spark jobs"""
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame


class BatchSessionHelper:
    """Helper for common spark actions and retrieving spark session"""

    def __init__(self, app_name: str):
        """
        :param app_name: Name of app for spark job
        :type app_name: str
        """
        conf = SparkConf().setAppName(app_name)
        self.spark = SparkSession.builder.config(conf=conf).getOrCreate()

    def read_csv_to_df(self, path: str, header_present: bool = True) -> DataFrame:
        """
        Selects csv data to a dataframe

        :param path: Absolute path to CSV file
        :type path: str
        :return: Table data
        :rtype: DataFrame
        """
        return self.spark.read.option("header", header_present).csv(path)

    def read_table_to_df(self, dbtable: str) -> DataFrame:
        """
        Selects table from postgres datawarehouse to a dataframe

        :param dbtable: Name of table to select from with format <schema>.<table_name>
        :type dbtable: str
        :return: Table data
        :rtype: DataFrame
        """
        return (
            self.spark.read.format("jdbc")
            .option("driver", "org.postgresql.Driver")
            .option("url", "jdbc:postgresql://datawarehouse/dw-blogs")
            .option("user", "user")
            .option("password", "password")
            .option("dbtable", dbtable)
            .load()
        )

    def write_df_to_table(self, df: DataFrame, dbtable: str) -> None:
        """
        Writes dataframe to table

        :param df: Data to insert into the table
        :type df: DataFrame
        :param dbtable: table to insert into
        :type dbtable: str
        """
        (
            df.write.format(
                "jdbc",
            )
            .mode("append")
            .option("driver", "org.postgresql.Driver")
            .option("url", "jdbc:postgresql://datawarehouse/dw-blogs")
            .option("user", "user")
            .option("password", "password")
            .option("dbtable", dbtable)
            .save()
        )
