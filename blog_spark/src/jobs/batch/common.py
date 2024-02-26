"""Helper methods and classes for spark jobs"""
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from requests import request


class BatchSessionHelper:
    """Helper for common spark actions and retrieving spark session"""

    def __init__(self, app_name: str):
        """
        :param app_name: Name of app for spark job
        :type app_name: str
        """
        conf = SparkConf().setAppName(app_name)
        self.spark = SparkSession.builder.config(conf=conf).getOrCreate()

    def get_vault_secret(self, vault_path: str):
        """
        Retrieves JSON secret from Vault

        :param vault_path: Path to secret in form of <engine>/<path>; ex: secret/test_secret
        :type vault_path: str
        """
        url = f"http://vault:8200/v2/{vault_path}"
        headers = {"content-type": "application/json", "Accept-Charset": "UTF-8", "X-Vault-Token": "token"}
        response = request.get(url, headers=headers)
        return response.json()

    def read_table_to_df(self, dbtable: str) -> DataFrame:
        """
        Selects table from postgres datawarehouse to a dataframe

        :param dbtable: Name of table to select from with format <schema>.<table_name>
        :type dbtable: str
        :return: Table data
        :rtype: DataFrame
        """
        secret = self.get_vault_secret("secret/connections/DATAWAREHOUSE")
        return (
            self.spark.read.format("jdbc")
            .option("driver", "org.postgresql.Driver")
            .option("url", "jdbc:postgresql://datawarehouse/dw-blogs")
            .option("user", "user")
            .option("password", secret["password"])
            .option("dbtable", dbtable)
            .load()
        )

    def write_df_to_table(self, df: DataFrame, dbtable: str, mode: str = "overwrite") -> None:
        """
        Writes dataframe to table

        :param df: Data to insert into the table
        :type df: DataFrame
        :param dbtable: Table to insert into
        :type dbtable: str
        :param mode: Mode for writing to table, defaults to "overwrite"
        :type mode: str, optional
        """
        (
            df.write.format(
                "jdbc",
            )
            .mode(mode)
            .option("driver", "org.postgresql.Driver")
            .option("url", "jdbc:postgresql://datawarehouse/dw-blogs")
            .option("user", "user")
            .option("password", "password")
            .option("dbtable", dbtable)
            .save()
        )
