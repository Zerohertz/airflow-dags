import airflow
from airflow.decorators import dag
from airflow.operators.bash import BashOperator


@dag(
    dag_id="Git-Status",
    start_date=airflow.utils.dates.days_ago(0),
    schedule_interval="*/15 * * * *",
    catchup=False,
)
def git_status():
    git_status = BashOperator(
        task_id="curl_status", bash_command=("curl {{ var.value.GITHUB_STATUS_URL }}"),
    )

    git_status


DAG = git_status()
