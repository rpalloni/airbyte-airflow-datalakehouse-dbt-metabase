from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1), # set date in the past to avoid double DAG run when unpause
}

dag = DAG(
    'dbt_transformer',
    default_args=default_args,
    schedule=timedelta(minutes=5),
    catchup=False, #  prevent backfilling DAG runs for past intervals back to start_date
    is_paused_upon_creation=False,  # ensures the DAG is active immediately upon creation without manual unpausing
    description='Run dbt transformer after data ingestion'
)


# the DockerOperator() is developed to create a new docker container on a docker server (local or remote server), and not to manage an existing container running.
# need to create the app image first and then create the new container based on that image the moment DockerOperator() is called

run_task = DockerOperator(
    task_id='run',
    image='transformer',
    command='dbt run',
    docker_url='unix://var/run/docker.sock', # allow airflow to access transformer container
    network_mode='kind', # allow transformer container and other containers communication
    auto_remove='success',  # automatically remove the container after it exits (comment to see the creation of a new container at each run)
    mount_tmp_dir=False,
    dag=dag,
)
