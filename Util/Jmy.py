import datetime as dt

from airflow.decorators import dag
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

from lib import Environment

ENV = Environment("JMY")


@dag(
    dag_id="JMY",
    start_date=dt.datetime(1998, 10, 23),
    schedule_interval="0 10 * * *",
    max_active_runs=1,
    catchup=False,
    tags=["FastAPI", "JMY"],
)
def JMY():
    JMY = KubernetesPodOperator(
        task_id="JMY",
        name="JMY",
        image="zerohertzkr/airflow-jmy",
        env_vars={
            "API_URI": ENV.API_URI,
            "ADMIN_EMAIL": ENV.ADMIN_EMAIL,
            "ADMIN_PASSWORD": ENV.ADMIN_PASSWORD,
        },
    )

    JMY


DAG = JMY()
