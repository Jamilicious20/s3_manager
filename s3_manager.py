import os
import boto3
from botocore.exceptions import ClientError

# Initialize the S3 client (automatically picks up environment variables)
s3_client = boto3.client('s3')
BUCKET_NAME = 'jamila-static-site'

def create_s3_bucket(bucket_name, region="eu-north-1"):
    """Creates a new S3 bucket."""
    try:
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"Bucket '{bucket_name}' created successfully!")
    except ClientError as e:
        print(f"Error creating bucket: {e}")

def upload_file_to_s3(local_file_path, s3_key):
    """Uploads a local file to the S3 bucket."""
    try:
        s3_client.upload_file(local_file_path, BUCKET_NAME, s3_key)
        print(f"Successfully uploaded '{local_file_path}' to s3://{BUCKET_NAME}/{s3_key}")
    except ClientError as e:
        print(f"Upload failed: {e}")

def extract_file_metadata(s3_key):
    """Retrieves and prints metadata and object headers from S3."""
    try:
        response = s3_client.head_object(Bucket=BUCKET_NAME, Key=s3_key)
        print(f"\n--- Metadata for {s3_key} ---")
        print(f"Content Type: {response.get('ContentType')}")
        print(f"File Size: {response.get('ContentLength')} bytes")
        print(f"Last Modified: {response.get('LastModified')}")
        print(f"ETag: {response.get('ETag')}")
    except ClientError as e:
        print(f"Could not retrieve metadata: {e}")

def download_file_from_s3(s3_key, local_download_path):
    """Downloads a file from S3 to your local machine."""
    try:
        s3_client.download_file(BUCKET_NAME, s3_key, local_download_path)
        print(f"Successfully downloaded s3://{BUCKET_NAME}/{s3_key} to '{local_download_path}'")
    except ClientError as e:
        print(f"Download failed: {e}")

if __name__ == "__main__":
    # Since your bucket already exists from Assignment 1, you can leave bucket creation commented out.
    # create_s3_bucket(BUCKET_NAME)
    
    sample_file = "sample.txt"
    # Create a dummy local file for testing
    with open(sample_file, "w") as f:
        f.write("Hello Pynexia Technologies! Cloud storage automation test.")

    target_key = "documents/sample.txt"
    
    # Run operations
    upload_file_to_s3(sample_file, target_key)
    extract_file_metadata(target_key)
    download_file_from_s3(target_key, "downloaded_sample.txt")