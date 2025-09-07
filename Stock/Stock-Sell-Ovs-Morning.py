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
    dag_id="Stock-Sell-Ovs-Morning",
    start_date=dt.datetime(1998, 10, 23),
    schedule_interval="10 7 * * 2-6",
    max_active_runs=1,
    catchup=False,
    tags=["zerohertzLib", "Discord", "Stock"],
)
def Stock():
    Stock_sell = KubernetesPodOperator(
        task_id="Stock-Sell",
        name="Stock-Sell",
        image="zerohertzkr/airflow-stock-sell",
        env_vars={
            "NORMAL": ENV.NORMAL,
            "START_DAY": ENV.START_DAY,
            "DISCORD_BOT_TOKEN": ENV.DISCORD_BOT_TOKEN,
            "DISCORD_BOT_CHANNEL": ENV.DISCORD_BOT_CHANNEL["ovs"],
            "MP_NUM": ENV.MP_NUM,
            "KOR": "0",
        },
        volumes=[volume_config],
        volume_mounts=[volume_mount],
    )
    Stock_balance = KubernetesPodOperator(
        task_id="Stock-Balance",
        name="Stock-Balance",
        image="zerohertzkr/airflow-stock-v4",
        env_vars={
            "NORMAL": ENV.NORMAL,
            "ISA": ENV.ISA,
            "DISCORD_BOT_TOKEN": ENV.DISCORD_BOT_TOKEN,
            "DISCORD_BOT_CHANNEL": ENV.DISCORD_BOT_CHANNEL["balance"],
        },
        volumes=[volume_config],
        volume_mounts=[volume_mount],
    )

    Stock_sell >> Stock_balance


DAG = Stock()
