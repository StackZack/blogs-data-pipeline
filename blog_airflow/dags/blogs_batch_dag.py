import datetime

from airflow.operators.empty import EmptyOperator

from airflow import DAG

my_dag = DAG(
    dag_id="my_dag_name",
    start_date=datetime.datetime(2024, 2, 6),
    schedule="@hourly",
)

EmptyOperator(task_id="task", dag=my_dag)
