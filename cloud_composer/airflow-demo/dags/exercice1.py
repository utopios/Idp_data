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
def extract():
    print("This is the extract task!")
    data = [
        {'name': 'Alice', 'age': 30},
        {'name': 'Bob', 'age': 25},
        {'name': 'Charlie', 'age': 35}
    ]
    return data

@task
def transform(data):
    """
    Filtrer les personnes dont l'âge est supérieur à 30 ans
    et convertir les noms en majuscules.
    """
    print("This is the transform task!")
    transformed_data = [
        {'name': person['name'].upper(), 'age': person['age']}
        for person in data if person['age'] > 30
    ]
    return transformed_data

@task
def load(data):
    """
    Ecrire les données transformées dans un fichier cdv local.
    """
    print("This is the load task!")
    with open('/tmp/transformed_data.csv', 'w') as f:
        f.write('name,age\n')
        for person in data:
            f.write(f"{person['name']},{person['age']}\n")
@dag('etl_pipeline',
            default_args=default_args, 
            schedule='0 0 * * *', 
            catchup=False,
            tags=['demo']
            )
def etl_dag():
    data = extract()
    transformed_data = transform(data)
    load(transformed_data)
dag = etl_dag()