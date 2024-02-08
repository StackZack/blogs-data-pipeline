import datetime

from airflow import DAG
from airflow.providers.sftp.operators.sftp import SFTPOperator

dag = DAG(
    dag_id="blogs_batch_load",
    start_date=datetime.datetime(2024, 2, 6),
    schedule=None,
)

SFTPOperator(
    task_id="blogs_sftp_to_nfs",
    dag=dag,
    operation="get",
    ssh_conn_id="INBOUND_SFTP",
    local_filepath="/home/airflow/shared/data/blogs.csv",
    remote_filepath="/upload/blogs.csv",
)
