import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.models.baseoperator import chain
from airflow.operators.empty import EmptyOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator

dag_params = Variable.get("blogs_batch_load_params")
spark_job_params = dag_params["spark_job_params"]
sftp_extract_tasks = []

dag = DAG(
    dag_id="blogs_batch_load",
    start_date=datetime.datetime(2024, 2, 6),
    schedule=None,
    default_args=dag_params["default_args"],
)

for file_name in dag_params["files"]:
    name = file_name.split(".csv")[0]
    extract_sftp = SFTPOperator(
        task_id=f"download_{name}_file",
        dag=dag,
        operation="get",
        ssh_conn_id=dag_params["ssh_conn_id"],
        local_filepath=f"/shared/data/{name}_{{{{ ts_nodash }}}}.csv",
        remote_filepath=f"/upload/{file_name}",
    )
    sftp_extract_tasks.append(extract_sftp)

load_stage_tables = SparkSubmitOperator(
    task_id="load_stage_tables",
    conn_id=dag_params["spark_conn_id"],
    application=f"{dag_params['spark_file_path']}/main.py",
    py_files=f"{dag_params['spark_file_path']}/jobs.zip",
    jars=f"{dag_params['spark_drivers_path']}/postgresql-42.7.1.jar",
    num_executors=spark_job_params["num_executors"],
    executor_cores=spark_job_params["executor_cores"],
    executor_memory=spark_job_params["executor_memory"],
    total_executor_cores=spark_job_params["total_executor_cores"],
    driver_memory=spark_job_params["driver_memory"],
    application_args=["--job", "load_blog_stage_tables", "--jobtype", "batch", "--jobts", "{{ ts_nodash }}"],
)

load_users = SQLExecuteQueryOperator(
    task_id="load_users",
    dag=dag,
    conn_id=dag_params["postgres_conn_id"],
    sql="./sql/gold_users.sql",
    params={"stage_schema": "staging", "gold_schema": "gold"},
)

load_blogs = SQLExecuteQueryOperator(
    task_id="load_blogs",
    dag=dag,
    conn_id=dag_params["postgres_conn_id"],
    sql="./sql/gold_blogs.sql",
    params={"stage_schema": "staging", "gold_schema": "gold"},
)

load_tag_lookup = SQLExecuteQueryOperator(
    task_id="load_tag_lookup",
    dag=dag,
    conn_id=dag_params["postgres_conn_id"],
    sql="./sql/gold_tag_lookup.sql",
    params={"stage_schema": "staging", "gold_schema": "gold"},
)

join_pre_req_tables = EmptyOperator(task_id="join_pre_req_tables", dag=dag)

load_comments = SQLExecuteQueryOperator(
    task_id="load_comments",
    dag=dag,
    conn_id=dag_params["postgres_conn_id"],
    sql="./sql/gold_comments.sql",
    params={"stage_schema": "staging", "gold_schema": "gold"},
)

load_favorites = SQLExecuteQueryOperator(
    task_id="load_favorites",
    dag=dag,
    conn_id=dag_params["postgres_conn_id"],
    sql="./sql/gold_favorites.sql",
    params={"stage_schema": "staging", "gold_schema": "gold"},
)

load_opinions = SQLExecuteQueryOperator(
    task_id="load_opinions",
    dag=dag,
    conn_id=dag_params["postgres_conn_id"],
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
