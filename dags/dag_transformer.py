import os
import pendulum
from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    'owner': 'airflow',
    # dynamic start_date so no past interval exists; DAG waits for next scheduled time
    # do not use in production to have reliable run history
    'start_date': pendulum.now('UTC') # datetime(2026, 1, 1),
}

dag = DAG(
    'dbt_transformer',
    default_args=default_args,
    schedule='15,45 * * * *', # run at :15 and :45 of every hour (15 mins after Airbyte ingests new data)
    catchup=False, #  prevent backfilling DAG runs for past intervals back to start_date
    is_paused_upon_creation=False,  # ensures the DAG is active immediately upon creation without manual unpausing
    description='Run dbt transformer after data ingestion'
)

start = BashOperator(
    task_id='wait_1_minute',
    bash_command='sleep 60',
    dag=dag,
)

# the DockerOperator() is developed to create a new docker container on a docker server (local or remote server), and not to manage an existing container running.
# need to create the transformer image first and then create the new container based on that image the moment DockerOperator() is called during DAG execution

run_task = DockerOperator(
    task_id='run_dbt',
    image='transformer',
    command='dbt run -s +rpt_user_stats',
    docker_url='unix:///var/run/docker.sock', # airflow worker access to docker socket to reach the Docker engine and create the container from the transformer image
    network_mode='kind', # allow transformer container and other containers communication
    auto_remove='success',  # automatically remove the container after it exits (comment to see the creation of a new container at each run)
    mount_tmp_dir=False,
    environment={
        'DREMIO_SPACE': os.environ.get('DREMIO_SPACE'),
        'DREMIO_SPACE_FOLDER': os.environ.get('DREMIO_SPACE_FOLDER'),
        'OBJECT_STORAGE_SOURCE': os.environ.get('OBJECT_STORAGE_SOURCE'),
        'OBJECT_STORAGE_PATH': os.environ.get('OBJECT_STORAGE_PATH'),
        'DREMIO_USER': os.environ.get('DREMIO_USER'),
        'DREMIO_PASSWORD': os.environ.get('DREMIO_PASSWORD'),
    },
    dag=dag,
)

end = EmptyOperator(task_id='workflow_end', dag=dag)

start >> run_task >> end