from airflow.hooks.base_hook import BaseHook
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from pprint import pprint
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import Session

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
def connect_to_db(ds, **kwargs):
    connection_string = BaseHook.get_connection('fitbit-connector').get_uri()

    engine = create_engine(connection_string)
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    
    Fitbit = Base.classes.fitbit
    session = Session(engine)
    user_ids = [user.fitbit_id for user in session.query(Fitbit).all()]
    print(user_ids)

    session.close()

run_this = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=connect_to_db,
    dag=dag,
)

run_this