"""Common fixtures"""
import json
from pathlib import Path

import pytest
from airflow.models import Variable


@pytest.fixture(name="patch_get_variable")
def patch_get_variable(mocker) -> None:
    """Mocks the airflow get variable call"""
    with open(f"{Path(__file__).parent}/data/variables.json") as json_file:
        dag_params = json.load(json_file)["blogs_batch_load_params"]
        return mocker.patch.object(
            Variable,
            "get",
            return_value=dag_params,
        )
