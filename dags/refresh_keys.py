from airflow.hooks.base_hook import BaseHook
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from pprint import pprint

conn = BaseHook.get_connection('fitbit-connector')
print(f"AIRFLOW_CONN_{conn.conn_id.upper()}='{conn.get_uri()}'")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2015, 6, 1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG(
    dag_id='refresh_keys',
    default_args=default_args,
    schedule_interval=None,
    tags=['example']
)


# [START howto_operator_python]
def print_context(ds, **kwargs):
    print('hello world')
    print(f"AIRFLOW_CONN_{conn.conn_id.upper()}='{conn.get_uri()}'")
    # return 'Whatever you return gets printed in the logs'
    return f"AIRFLOW_CONN_{conn.conn_id.upper()}='{conn.get_uri()}'"

run_this = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=print_context,
    dag=dag,
)

run_this