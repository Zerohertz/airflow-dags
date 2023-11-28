import datetime as dt
import json

from airflow.decorators import dag
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

from lib import Environment

ENV = Environment("GA4")


@dag(
    dag_id="GA-4-Daily",
    start_date=dt.datetime(1998, 10, 23),
    schedule_interval="0 10 * * *",
    max_active_runs=1,
    catchup=False,
    tags=["Discord", "Google Analytics 4"],
)
def GA4():
    GA4 = KubernetesPodOperator(
        task_id="GA4",
        name="GA4",
        image="zerohertzkr/airflow-ga4",
        env_vars={
            "KEY": json.dumps(ENV.KEY),
            "PROPERTY_ID": ENV.PROPERTY_ID,
            "WEBHOOK": ENV.WEBHOOK,
            "PER": "1",
        },
    )

    GA4


DAG = GA4()
