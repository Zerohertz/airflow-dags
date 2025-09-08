import datetime as dt

from airflow.decorators import dag
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from lib import Environment

ENV = Environment("STOCK")


@dag(
    dag_id="Stock-Buy-Ovs",
    start_date=dt.datetime(1998, 10, 23),
    schedule_interval="45 23 * * 1-5",
    max_active_runs=1,
    catchup=False,
    tags=["zerohertzLib", "Discord", "Stock"],
)
def Stock():
    Stock = KubernetesPodOperator(
        task_id="Stock",
        name="Stock",
        image="zerohertzkr/airflow-stock-buy",
        env_vars={
            "SYMBOLS": ENV.SYMBOLS,
            "START_DAY": ENV.START_DAY,
            "TOP": ENV.TOP,
            "DISCORD_BOT_TOKEN": ENV.DISCORD_BOT_TOKEN,
            "DISCORD_BOT_CHANNEL": ENV.DISCORD_BOT_CHANNEL["ovs"],
            "MP_NUM": ENV.MP_NUM,
            "KOR": "0",
        },
    )


DAG = Stock()
