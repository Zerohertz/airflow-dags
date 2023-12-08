import datetime as dt

from airflow.decorators import dag
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

from lib import Environment

ENV = Environment("STOCK")


@dag(
    dag_id="Stock-Quant-Kor",
    start_date=dt.datetime(1998, 10, 23),
    schedule_interval="30 9,13 * * 1-5",
    max_active_runs=1,
    catchup=False,
    tags=["zerohertzLib", "Slack", "Stock"],
)
def Stock():
    Stock = KubernetesPodOperator(
        task_id="Stock",
        name="Stock",
        image="zerohertzkr/airflow-quant",
        env_vars={
            "SYMBOLS": "100",
            "SLACK": ENV.SLACK,
            "START_DAY": "20200101",
            "TOP": "4",
            "MP_NUM": "8",
            "KOR": "1",
        },
    )

    Stock


DAG = Stock()
