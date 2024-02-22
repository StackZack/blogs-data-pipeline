# blogs-data-pipeline

## Getting Started

### Requirements

For dev work this repo requires that the **pre-commit** package is installed ([info here](https://pre-commit.com/#install)).

### Development

Within a virtual environment run the below commands.

```bash
pip install -r requirements-dev.txt
pre-commit install
```

load_stage_table = PostgresOperator(
    task_id=f"load_{name}_stage_table",
    dag=dag,
    postgres_conn_id="DATAWAREHOUSE",
    sql="./sql/stage_load.sql",
    params={
        "table_name": f"staging.stg_{name}",
        "csv_file_path": f"/shared/{file_name}",
    },
)
