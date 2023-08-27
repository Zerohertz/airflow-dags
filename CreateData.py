import datetime as dt

import airflow
import numpy as np
from airflow.decorators import dag
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from dateutil.parser import parse

CLASSES = ["A", "B"]
NO_DATA = 10


def _mean(time, class_name):
    idx = CLASSES.index(class_name)
    time /= 12
    if idx == 0:
        mean_x = time
    elif idx == 1:
        mean_x = 2 - time
    mean_y = time ** 2
    return mean_x, mean_y


def _generate_queries(class_name, num_entries, ts):
    queries = []
    mean_x, mean_y = _mean(int(ts[11:13]), class_name)
    print("=" * 10)
    ts = parse(ts)
    for _ in range(num_entries):
        x = np.random.normal(mean_x, 1)
        y = np.random.normal(mean_y, 1)
        queries.append(
            f"INSERT INTO CONTINUOUS_TRAINING (time, x, y, class) VALUES ('{ts.strftime('%Y-%m-%d %H:%M:%S%z')}', {x}, {y}, '{class_name}');"
        )
    return "\n".join(queries)


def _merge_queries(ti):
    queries = []
    for c in CLASSES:
        queries.append(ti.xcom_pull(task_ids=f"generate_data_{c}"))
    return "\n".join(queries)


@dag(
    dag_id="Create-Data",
    start_date=airflow.utils.dates.days_ago(2),
    schedule_interval="@hourly",
    max_active_runs=1,
    catchup=True,
    tags=["MLOps", "Data Engineering"],
)
def create_data():
    create_table = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="zerohertz-db",
        sql="""
        CREATE TABLE IF NOT EXISTS
        CONTINUOUS_TRAINING (
            time TIMESTAMP NOT NULL,
            x FLOAT NOT NULL,
            y FLOAT NOT NULL,
            class TEXT NOT NULL
        );
        """,
    )

    generate_queries = []

    for c in CLASSES:
        generate_query = PythonOperator(
            task_id=f"generate_data_{c}",
            python_callable=_generate_queries,
            op_args=[c, NO_DATA],
            do_xcom_push=True,
        )
        generate_queries.append(generate_query)

    merge_queries = PythonOperator(
        task_id=f"merge_queries", python_callable=_merge_queries, do_xcom_push=True,
    )

    push_data = PostgresOperator(
        task_id=f"push_data",
        postgres_conn_id="zerohertz-db",
        sql="{{ ti.xcom_pull(task_ids='merge_queries', key='return_value') }}",
    )

    create_table >> generate_queries >> merge_queries >> push_data


DAG = create_data()
