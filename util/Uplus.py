import datetime as dt

from airflow.decorators import dag
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from lib import Environment

ENV = Environment("UPLUS")


@dag(
    dag_id="Uplus",
    start_date=dt.datetime(1998, 10, 23),
    schedule_interval="0 9 * * *",
    max_active_runs=1,
    catchup=False,
    tags=["Discord"],
)
def Uplus():
    Uplus = KubernetesPodOperator(
        task_id="Uplus",
        name="Uplus",
        image="zerohertzkr/airflow-uplus",
        env_vars={
            "WEBHOOK": ENV.WEBHOOK,
            "USER_ID": ENV.USER_ID,
            "USER_PASSWORD": ENV.USER_PASSWORD,
            "CARD_NO": ENV.CARD_NO,
            "NAME": ENV.NAME,
            "BIRTH": ENV.BIRTH,
            "CARD_YEAR": ENV.CARD_YEAR,
            "CARD_MONTH": ENV.CARD_MONTH,
        },
    )

    Uplus


DAG = Uplus()
