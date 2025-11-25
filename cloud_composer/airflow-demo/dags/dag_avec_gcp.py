from airflow.decorators import dag, task
from airflow.providers.google.cloud.hooks.gcs import GCSHook
GCP_CONN_ID= "gcp_default"

BUCKET_NAME = "ihab_bucket_utopios"


@task
def write_to_gcs(**kwargs):
    

    gcs_hook = GCSHook(gcp_conn_id=GCP_CONN_ID)
    data = "Hello, World!"
    gcs_hook.upload(
        bucket_name=BUCKET_NAME,
        object_name="hello_world.txt",
        data=data,
        mime_type="text/plain"
    )
    print(f"File uploaded to gs://{BUCKET_NAME}/hello_world.txt")

@dag(
    dag_id="dag_avec_gcp",
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["example", "gcp"],
)
def gcp_dag_example():
    write_to_gcs_task = write_to_gcs()
    
gcp_dag = gcp_dag_example()