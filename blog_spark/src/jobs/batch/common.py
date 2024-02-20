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
        conf = (
            SparkConf().setAppName(app_name).set("spark.jars", "/opt/bitnami/spark/jars/drivers/postgresql-42.7.1.jar")
        )
        self.spark = SparkSession.builder.config(conf=conf).getOrCreate()

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
            .option("url", "jdbc:postgresql://datawarehouse/dw-blogs")
            .option("user", "user")
            .option("password", "password")
            .option("dbtable", dbtable)
            .load()
        )
