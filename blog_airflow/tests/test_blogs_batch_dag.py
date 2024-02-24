import pytest
from airflow.hooks.base import BaseHook
from airflow.models.connection import Connection
from airflow.providers.common.sql.hooks.sql import DbApiHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.sftp.hooks.sftp import SFTPHook

file_names = ["blogs", "comments", "favorites", "opinions", "blog_tags", "tags", "users"]
table_names = ["blogs", "tag_lookup", "comments", "favorites", "opinions"]


@pytest.mark.parametrize("file_name", file_names)
def test_sftp_download(file_name, mocker, patch_get_variable):
    """Asserts that retrieve_file is called and that the arguments are correct"""
    patch_get_variable()
    from blog_airflow.dags import blogs_batch_dag

    # Retrieve task from DAG
    dag = blogs_batch_dag.dag
    task = dag.get_task(f"download_{file_name}_file")

    # Patch call to retrieve connection
    mocker.patch.object(
        BaseHook,
        "get_connection",
        return_value=Connection(conn_type="sftp", host="localhost", login="test", password="test"),
    )

    # Mock expected call to retrieve_file and assert arguments
    mock_retrieve_file = mocker.patch.object(SFTPHook, "retrieve_file")
    task.execute(context={})
    assert f"/upload/{file_name}.csv" == mock_retrieve_file.call_args_list[0][0][0]
    assert f"/shared/data/{file_name}_{{{{ ts_nodash }}}}.csv" == mock_retrieve_file.call_args_list[0][0][1]


@pytest.mark.parametrize("table_name", table_names)
def test_gold_load(table_name, mocker, patch_get_variable):
    """Asserts that correct arguments are passed to stage tasks"""
    patch_get_variable()
    from blog_airflow.dags import blogs_batch_dag

    # Retrieve task from DAG
    dag = blogs_batch_dag.dag
    task = dag.get_task(f"load_{table_name}")

    # Patch call to retrieve connection
    mocker.patch.object(
        BaseHook,
        "get_connection",
        return_value=Connection(conn_type="postgres", host="localhost", login="test", password="test", schema="test"),
    )

    # Mock expected calls to Postgres hooks and SQL executions and assert arguments
    mocker.patch.object(PostgresHook, "get_conn")
    mocker.patch.object(PostgresHook, "_get_cursor")
    mock_sql_run = mocker.patch.object(DbApiHook, "_run_command")
    task.execute(context={})
    # TODO: Add more assertions on rendered SQL and properly check parameters
    assert ".sql" in mock_sql_run.call_args_list[0][0][1]
