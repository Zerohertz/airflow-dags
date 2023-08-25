import datetime as dt

from airflow.decorators import dag
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)


@dag(
    dag_id="GA-4",
    start_date=dt.datetime(1998, 10, 23),
    schedule_interval="0 1 * * *",
    max_active_runs=1,
    catchup=False,
)
def GA4():
    GA4 = KubernetesPodOperator(task_id="GA4", name="GA4", image="airflow-ga4:v1",)

    GA4


DAG = GA4()
