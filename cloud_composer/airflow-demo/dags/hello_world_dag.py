### Hello world DAG for apache Airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
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

def first_task():
    print("This is the first task!")

def second_task():
    print("This is the second task!")

with DAG('hello_world', 
         default_args=default_args, 
         schedule='0 0 * * *', 
         catchup=False,
         tags=['demo']
        ) as dag:
    hello_task = BashOperator(
        task_id='hello_task',
        bash_command='echo "Hello, World!"'
    )

    task_python_1 = PythonOperator(
        task_id='task_python',
        python_callable=first_task
    )

    task_python_2 = PythonOperator(
        task_id='task_python_2',
        python_callable=second_task
    )

    hello_task >> task_python_1 >> task_python_2
 