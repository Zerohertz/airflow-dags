import datetime as dt

from airflow.decorators import dag
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)


@dag(
    dag_id="Uplus",
    start_date=dt.datetime(1998, 10, 23),
    schedule_interval="0 0 * * *",
    max_active_runs=1,
    catchup=False,
)
def Uplus():
    Uplus = KubernetesPodOperator(
        task_id="Uplus", name="Uplus", image="airflow-uplus:v1",
    )

    Uplus


DAG = Uplus()
