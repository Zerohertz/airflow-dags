import datetime as dt
import json

from airflow.decorators import dag
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

from lib import Environment

ENV = Environment("GA4")


@dag(
    dag_id="GA-4-Montly",
    start_date=dt.datetime(1998, 10, 23),
    schedule_interval="0 11 1,11,21 * *",
    max_active_runs=1,
    catchup=False,
    tags=["zerohertzLib", "Slack", "Google Analytics 4"],
)
def GA4():
    GA4 = KubernetesPodOperator(
        task_id="GA4",
        name="GA4",
        image="zerohertzkr/airflow-ga4",
        env_vars={
            "KEY": json.dumps(ENV.KEY),
            "PROPERTY_ID": ENV.PROPERTY_ID,
            "SLACK": ENV.SLACK,
            "PER": "30",
        },
    )

    GA4


DAG = GA4()
