import airflow
from airflow.decorators import dag
from airflow.operators.bash import BashOperator

from lib import Environment

ENV = Environment("GITHUB-STATUS")


@dag(
    dag_id="Git-Status",
    start_date=airflow.utils.dates.days_ago(0),
    schedule_interval="*/15 * * * *",
    catchup=False,
    tags=["GitHub"],
)
def git_status():
    git_status = BashOperator(
        task_id="curl_status",
        bash_command=(f"curl {ENV.STATUS_URL}"),
    )

    git_status


DAG = git_status()
