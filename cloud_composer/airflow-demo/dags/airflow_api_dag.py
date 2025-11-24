### Hello world DAG for apache Airflow
from airflow import DAG
from airflow.decorators import task, dag
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import time
from datetime import datetime
default_args = {
    'owner': 'Ihab',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 3,
    'retry_delay': 300,
    'start_date': datetime(2025, 11, 20),
    'end_date': datetime(2025, 12, 1),
}

@task
def first_task():
    print("This is the first task!")

@task
def second_task():
    print("This is the second task!")


@dag('airflow_api_dag', 
         default_args=default_args, 
         schedule='0 0 * * *', 
         catchup=False,
         tags=['demo']
        )
def first_dag():
    hello_task = BashOperator(
        task_id='hello_task',
        bash_command='echo "Hello, World!" && sleep 10'
    )

    hello2_task = BashOperator(
        task_id='hello_task_2',
        bash_command='echo "Hello, World!" && sleep 10'
    )

    
    task_python_1 = first_task()
    task_python_2 = second_task()

    hello_task >> [task_python_1, task_python_2] >> hello2_task

dag = first_dag()

 