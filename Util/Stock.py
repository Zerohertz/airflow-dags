import datetime as dt

from airflow.decorators import dag
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from kubernetes.client.models import V1Volume, V1VolumeMount

from lib import Environment

ENV = Environment("STOCK")

volume_config = V1Volume(
    name="stock-pvc",
    persistent_volume_claim={"claimName": "airflow-stock-pvc"},
)
volume_mount = V1VolumeMount(name="stock-pvc", mount_path="/app/data", read_only=True)


@dag(
    dag_id="Stock",
    start_date=dt.datetime(1998, 10, 23),
    schedule_interval="1,31 9-15 * * 1-5",
    max_active_runs=1,
    catchup=False,
    tags=["zerohertzLib", "Slack"],
)
def Stock():
    Stock = KubernetesPodOperator(
        task_id="Stock",
        name="Stock",
        image="zerohertzkr/airflow-stock",
        env_vars={
            "SLACK": ENV.SLACK,
        },
        volumes=[volume_config],
        volume_mounts=[volume_mount],
    )

    Stock


DAG = Stock()
