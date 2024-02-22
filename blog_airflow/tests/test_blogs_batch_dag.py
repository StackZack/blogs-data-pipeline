import pytest
from airflow.hooks.base import BaseHook
from airflow.models.connection import Connection
from airflow.providers.common.sql.hooks.sql import DbApiHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.sftp.hooks.sftp import SFTPHook

from blog_airflow.dags import blogs_batch_dag

file_names = ["blogs", "comments", "favorites", "opinions", "blog_tags", "tags", "users"]


@pytest.mark.parametrize("file_name", file_names)
def test_sftp_download(file_name, mocker):
    """Asserts that retrieve_file is called and that the arguments are correct"""
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
    assert f"/shared/data/{file_name}.csv" == mock_retrieve_file.call_args_list[0][0][1]


@pytest.mark.parametrize("file_name", file_names)
def test_stage_load(file_name, mocker):
    """Asserts that correct arguments are passed to stage tasks"""
    # Retrieve task from DAG
    dag = blogs_batch_dag.dag
    task = dag.get_task(f"load_{file_name}_stage_table")
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
    # TODO: Add more assertions on rendered SQL
    assert "./sql/stage_load.sql" == mock_sql_run.call_args_list[0][0][1]
