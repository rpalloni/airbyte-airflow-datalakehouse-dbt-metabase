from dags.dag_transformer import dag
from airflow.providers.docker.operators.docker import DockerOperator


def test_dag_loads():
    assert dag is not None
    assert dag.dag_id == "dbt_transformer"


def test_dag_task_count():
    assert len(dag.tasks) == 4


def test_dag_task_ids():
    task_ids = {t.task_id for t in dag.tasks}
    assert task_ids == {"wait_1_minute", "run_dbt", "test_dbt", "workflow_end"}


def test_dag_task_dependencies():
    run_dbt = dag.get_task("run_dbt")
    test_dbt = dag.get_task("test_dbt")
    assert "wait_1_minute" in {t.task_id for t in run_dbt.upstream_list}
    assert "test_dbt" in {t.task_id for t in run_dbt.downstream_list}
    assert "run_dbt" in {t.task_id for t in test_dbt.upstream_list}
    assert "workflow_end" in {t.task_id for t in test_dbt.downstream_list}


def test_dag_schedule():
    assert dag.schedule == "15,45 * * * *"


def test_dag_no_catchup():
    assert dag.catchup is False


def test_run_dbt_command():
    run_dbt = dag.get_task("run_dbt")
    assert isinstance(run_dbt, DockerOperator)
    command = str(run_dbt.command)
    assert "dbt run" in command
    assert "rpt_user_stats" in command


def test_test_dbt_command():
    test_dbt = dag.get_task("test_dbt")
    assert isinstance(test_dbt, DockerOperator)
    command = str(test_dbt.command)
    assert "dbt test" in command


def test_docker_tasks_share_image():
    run_dbt = dag.get_task("run_dbt")
    test_dbt = dag.get_task("test_dbt")
    assert isinstance(run_dbt, DockerOperator)
    assert isinstance(test_dbt, DockerOperator)
    assert run_dbt.image == test_dbt.image == "transformer"


def test_docker_tasks_share_network():
    run_dbt = dag.get_task("run_dbt")
    test_dbt = dag.get_task("test_dbt")
    assert isinstance(run_dbt, DockerOperator)
    assert isinstance(test_dbt, DockerOperator)
    assert run_dbt.network_mode == test_dbt.network_mode == "kind"


def test_run_dbt_env_keys():
    run_dbt = dag.get_task("run_dbt")
    assert isinstance(run_dbt, DockerOperator)
    required_keys = {
        "DREMIO_SPACE",
        "DREMIO_SPACE_FOLDER",
        "OBJECT_STORAGE_SOURCE",
        "OBJECT_STORAGE_PATH",
        "DREMIO_USER",
        "DREMIO_PASSWORD",
    }
    assert required_keys.issubset(run_dbt.environment.keys())
