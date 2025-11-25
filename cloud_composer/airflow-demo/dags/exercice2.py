from datetime import datetime, timedelta

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
        return False, f"Invalid records exceed threshold: {invalid_ratio:.2%} > {INVALID_THRESHOLD:.2%}"

    return True, "All records are valid within the acceptable threshold."

def process_and_validate_sales():
    pass

def check_quality_threshold():
    pass
