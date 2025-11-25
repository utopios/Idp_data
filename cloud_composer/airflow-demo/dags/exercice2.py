from datetime import datetime, timedelta
import json
from airflow.decorators import dag, task, task_group
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook

GCP_CONN_ID= "google_default"
SOURCE_BUCKET = "raw-sales-bucket"
STAGING_BUCKET = "staging-sales-bucket"
TARGET_BUCKET = "curated-sales-bucket"
INVALID_THRESHOLD = 0.1  # 10% invalid records allowed

default_args = {
    'owner': 'Ihab',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False,
}


def validate_sales_record(records):
    """ Validate sales records.
        A valid record must have non-null 'sale_id', 'customer_id', 'country','amount', and 'sale_ts' fields.
        Save invalid records to a separate file in GCS if needed.
        Save valid records to another file in GCS if needed.
        Returns a tuple of (is_valid, error_message).

    """
    required_fields = ['sale_id', 'customer_id', 'country', 'amount', 'sale_ts']
    invalid_count = 0

    for record in records:
        if not all(field in record and record[field] is not None for field in required_fields):
            invalid_count += 1

    total_count = len(records)
    if total_count == 0:
        return False, "No records to validate."

    invalid_ratio = invalid_count / total_count
    if invalid_ratio > INVALID_THRESHOLD:
        gcs_hook = GCSHook(gcp_conn_id=GCP_CONN_ID)
        invalid_data = [record for record in records if not all(field in record and record[field
] is not None for field in required_fields)]
        invalid_data_str = json.dumps(invalid_data, indent=2)
        gcs_hook.upload(
            bucket_name=STAGING_BUCKET,
            object_name="invalid_records/invalid_sales_records.json",
            data=invalid_data_str,
            mime_type="application/json"
        )
        return False, f"Invalid records exceed threshold: {invalid_ratio:.2%} > {INVALID_THRESHOLD:.2%}"

    gcs_hook = GCSHook(gcp_conn_id=GCP_CONN_ID)
    valid_data = [record for record in records if all(field in record and record[field] is not None for field in required_fields)]
    valid_data_str = json.dumps(valid_data, indent=2)
    gcs_hook.upload(
        bucket_name=TARGET_BUCKET,
        object_name="valid_records/valid_sales_records.json",
        data=valid_data_str,
        mime_type="application/json"
    )
    return True, "All records are valid within the acceptable threshold."

@task_group(group_id="ingest_group")    
def ingest_group():
    check_file_task = GCSObjectExistenceSensor(
        task_id="check_file_existence",
        bucket=SOURCE_BUCKET,
        object="incoming/sales_2025-11-25.json",
        timeout = 600,
        poke_interval = 30,
        mode = 'poke',
        google_cloud_conn_id=GCP_CONN_ID,
    )

    copy_file = GCSToGCSOperator(
        task_id="copy_file_to_staging",
        source_bucket=SOURCE_BUCKET,
        source_object="incoming/sales_2025-11-25.json",
        destination_bucket=STAGING_BUCKET,
        destination_object="incoming/sales_2025-11-25.json",
        move_object=False,
        gcp_conn_id=GCP_CONN_ID
    )
    check_file_task >> copy_file
    return copy_file

@task_group(group_id="validation_group")
def validation_group():

    @task
    def notify_invalid_data(error_message: str):
        print(f"Data validation failed: {error_message}")
        # Here you could add email notification logic or other alerting mechanisms

    @task
    def read_file_from_statging():
        staging_file_ath= f"incoming/sales_2025_11_25.json"

        gcs_hook = GCSHook(gcp_conn_id=GCP_CONN_ID)
        file_content = gcs_hook.download(
            bucket_name=STAGING_BUCKET,
            object_name=staging_file_ath
        )
        records = json.loads(file_content)
        result = validate_sales_record(records)
        is_valid, message = result
        if not is_valid:
            notify_invalid_data(message)
        return is_valid
    return read_file_from_statging
    

@dag(
    dag_id="sales_data_pipeline",
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=["sales", "data_pipeline", "gcp"],
    start_date=datetime(2025, 1, 1),

)
def sales_data_pipeline():
    ingest = ingest_group()
    validate = validation_group()

    ingest >> validate()

sales_dag = sales_data_pipeline()
    

