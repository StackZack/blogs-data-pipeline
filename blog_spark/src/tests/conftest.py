"""Common fixtures"""
import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark() -> SparkSession:
    """Creates generic SparkSession for unit tests

    :return: Test session
    :rtype: SparkSession
    """
    return SparkSession.builder.master("local").appName("test_spark").getOrCreate()
