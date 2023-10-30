import datetime as dt

from airflow.decorators import dag
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

from lib import Environment

ENV = Environment("STOCK")


@dag(
    dag_id="Stock",
    start_date=dt.datetime(1998, 10, 23),
    schedule_interval="1,31 9-15 * * 1-5",
    max_active_runs=1,
    catchup=False,
    tags=["Discord"],
)
def Stock():
    Stock = KubernetesPodOperator(
        task_id="Stock",
        name="Stock",
        image="zerohertzkr/airflow-stock",
        env_vars={
            "WEBHOOK": ENV.WEBHOOK,
            "STOCK": str(ENV.STOCK),
        },
    )

    Stock


DAG = Stock()
