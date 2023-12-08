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
volume_mount = V1VolumeMount(name="stock-pvc", mount_path="/app/stock", read_only=False)


@dag(
    dag_id="Stock-Ovs-V2-Night",
    start_date=dt.datetime(1998, 10, 23),
    schedule_interval="40 23 * * 1-5",
    max_active_runs=1,
    catchup=False,
    tags=["zerohertzLib", "Slack", "Stock"],
)
def Stock():
    Stock = KubernetesPodOperator(
        task_id="Stock",
        name="Stock",
        image="zerohertzkr/airflow-stock-v2",
        env_vars={
            "SLACK": ENV.SLACK,
            "START_DAY": "20200101",
            "MP_NUM": "8",
            "KOR": "0",
        },
        volumes=[volume_config],
        volume_mounts=[volume_mount],
    )


DAG = Stock()
