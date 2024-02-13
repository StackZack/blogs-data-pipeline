import datetime

from airflow import DAG
from airflow.providers.sftp.operators.sftp import SFTPOperator

dag = DAG(
    dag_id="blogs_batch_load",
    start_date=datetime.datetime(2024, 2, 6),
    schedule=None,
)

files = ["blogs.csv", "comments.csv", "favorites.csv", "opinions.csv", "tags.csv", "users.csv"]

for file_name in files:
    name = file_name.split(".csv")[0]
    SFTPOperator(
        task_id=f"download_{name}_file",
        dag=dag,
        operation="get",
        ssh_conn_id="INBOUND_SFTP",
        local_filepath=f"/home/airflow/shared/{file_name}",
        remote_filepath=f"/upload/{file_name}",
    )
