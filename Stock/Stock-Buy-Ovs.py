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
    tags=["zerohertzLib", "Slack", "Stock"],
)
def Stock():
    Stock = KubernetesPodOperator(
        task_id="Stock",
        name="Stock",
        image="zerohertzkr/airflow-stock-buy",
        env_vars={
            "SLACK": ENV.SLACK,
            "SYMBOLS": "100",
            "START_DAY": "20200101",
            "TOP": "4",
            "MP_NUM": "10",
            "KOR": "0",
        },
    )


DAG = Stock()
