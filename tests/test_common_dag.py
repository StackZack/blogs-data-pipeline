"""General unit tests for DAGs
"""
import glob
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType

import pytest
from airflow.models.dag import DAG
from airflow.utils.dag_cycle_tester import check_cycle

DAG_DIR_PATH = Path(__file__).parent.parent.resolve() / "blog_airflow" / "dags"
DAG_GLOB_EXPR = DAG_DIR_PATH / "[!__init__]*.py"
DAG_NAMES = [Path(DAG_PATH).name for DAG_PATH in glob.glob(str(DAG_GLOB_EXPR))]


@pytest.mark.parametrize("dag_name", DAG_NAMES)
def test_dag_cycles(dag_name: str):
    """Asserts that each DAG can be imported and has no cycles

    :param dag_name: Name of file containing DAG
    :type dag_name: str
    """
    module = _import_file(dag_name, str(DAG_DIR_PATH / dag_name))
    dag_objects = [var for var in vars(module).values() if isinstance(var, DAG)]
    assert dag_objects
    for dag in dag_objects:
        check_cycle(dag)


def _import_file(module_name: str, module_path: str) -> ModuleType:
    """Gets module object from module path

    :param module_name: Name of module to load
    :type module_name: str
    :param module_path: Path of module to load
    :type module_path: str
    :return: Loaded module
    :rtype: ModuleType
    """
    spec = spec_from_file_location(module_name, str(module_path))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
