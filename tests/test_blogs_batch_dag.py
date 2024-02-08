from airflow.hooks.base import BaseHook
from airflow.models.connection import Connection
from airflow.providers.sftp.hooks.sftp import SFTPHook

from blog_airflow.dags import blogs_batch_dag


def test_sftp_to_nfs(mocker):
    """Asserts that retrieve_file is called and that the arguments are correct"""
    # Retrieve task from DAG
    dag = blogs_batch_dag.dag
    task = dag.get_task("blogs_sftp_to_nfs")
    # Patch call to retrieve connection
    mocker.patch.object(
        BaseHook,
        "get_connection",
        return_value=Connection(conn_type="sftp", host="localhost", login="test", password="test"),
    )
    # Mock expected call to retrieve_file and assert arguments
    mock_retrieve_file = mocker.patch.object(SFTPHook, "retrieve_file")
    task.execute(context={})
    assert "/upload/blogs.csv" == mock_retrieve_file.call_args_list[0][0][0]
    assert "/home/airflow/blogs.csv" == mock_retrieve_file.call_args_list[0][0][1]
