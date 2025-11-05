from google.cloud import storage
import os
client = storage.Client()
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/service-account-file.json"

# List all buckets in the project
buckets = client.list_buckets()
print("Buckets in project:")
for bucket in buckets:
    print(bucket.name)

# Access a specific bucket
bucket_name = "ihab_bucket_utopios"
bucket = client.bucket(bucket_name)
blobs = bucket.list_blobs()
for blob in blobs:
    print(blob.name)

# Upload a file to the bucket
blob = bucket.blob("new_data.csv")
blob.upload_from_filename("../data/to_upload.csv")

# Download a file from the bucket

blob = bucket.blob("data.csv")
blob.download_to_filename("../data/downloaded_data.csv")
