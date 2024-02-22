import datetime
from datetime import timedelta

from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.empty import EmptyOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator

default_args = {"retry_delay": timedelta(minutes=5), "email_on_failure": False, "email_on_retry": False, "retries": 1}

dag = DAG(
    dag_id="blogs_batch_load",
    start_date=datetime.datetime(2024, 2, 6),
    schedule=None,
    default_args=default_args,
)

files = ["blogs.csv", "comments.csv", "favorites.csv", "opinions.csv", "blog_tags.csv", "tags.csv", "users.csv"]

spark_job_params = {
    "num_executors": 1,
    "executor_cores": 1,
    "executor_memory": "512M",
    "total_executor_cores": 1,
    "driver_memory": "512M",
}

sftp_extract_tasks = []

for file_name in files:
    name = file_name.split(".csv")[0]
    extract_sftp = SFTPOperator(
        task_id=f"download_{name}_file",
        dag=dag,
        operation="get",
        ssh_conn_id="INBOUND_SFTP",
        local_filepath=f"/shared/data/{file_name}",
        remote_filepath=f"/upload/{file_name}",
    )
    sftp_extract_tasks.append(extract_sftp)

load_stage_tables = SparkSubmitOperator(
    task_id="load_stage_tables",
    conn_id="SPARK",
    application="/opt/airflow/spark/dist/main.py",
    py_files="/opt/airflow/spark/dist/jobs.zip",
    jars="/opt/airflow/dags/jars/drivers/postgresql-42.7.1.jar",
    num_executors=spark_job_params["num_executors"],
    executor_cores=spark_job_params["executor_cores"],
    executor_memory=spark_job_params["executor_memory"],
    total_executor_cores=spark_job_params["total_executor_cores"],
    driver_memory=spark_job_params["driver_memory"],
    application_args=[
        "--job",
        "load_blog_stage_tables",
        "--jobtype",
        "batch",
    ],
)

load_users = PostgresOperator(
    task_id="load_users",
    dag=dag,
    postgres_conn_id="DATAWAREHOUSE",
    sql="./sql/gold_users.sql",
    params={"stage_schema": "staging", "gold_schema": "gold"},
)

load_blogs = PostgresOperator(
    task_id="load_blogs",
    dag=dag,
    postgres_conn_id="DATAWAREHOUSE",
    sql="./sql/gold_blogs.sql",
    params={"stage_schema": "staging", "gold_schema": "gold"},
)

load_tag_lookup = PostgresOperator(
    task_id="load_tag_lookup",
    dag=dag,
    postgres_conn_id="DATAWAREHOUSE",
    sql="./sql/gold_tag_lookup.sql",
    params={"stage_schema": "staging", "gold_schema": "gold"},
)

join_pre_req_tables = EmptyOperator(task_id="join_pre_req_tables", dag=dag)

load_comments = PostgresOperator(
    task_id="load_comments",
    dag=dag,
    postgres_conn_id="DATAWAREHOUSE",
    sql="./sql/gold_comments.sql",
    params={"stage_schema": "staging", "gold_schema": "gold"},
)

load_favorites = PostgresOperator(
    task_id="load_favorites",
    dag=dag,
    postgres_conn_id="DATAWAREHOUSE",
    sql="./sql/gold_favorites.sql",
    params={"stage_schema": "staging", "gold_schema": "gold"},
)

load_opinions = PostgresOperator(
    task_id="load_opinions",
    dag=dag,
    postgres_conn_id="DATAWAREHOUSE",
    sql="./sql/gold_opinions.sql",
    params={"stage_schema": "staging", "gold_schema": "gold"},
)

chain(
    sftp_extract_tasks,
    load_stage_tables,
    load_users,
    [load_blogs, load_tag_lookup],
    join_pre_req_tables,
    [load_comments, load_favorites, load_opinions],
)
