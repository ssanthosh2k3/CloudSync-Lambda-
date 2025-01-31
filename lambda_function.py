import json
import boto3
import os
import io
from minio import Minio
from minio.error import S3Error

# AWS S3 Client
s3_client = boto3.client('s3')

# MinIO Client Configuration
MINIO_ENDPOINT = "objectstore.e2enetworks.net"  # ✅ Remove "https://"
MINIO_ACCESS_KEY = "your-key"
MINIO_SECRET_KEY = "your-key"
MINIO_BUCKET = "backup-23"

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=True  # Change to False if using HTTP
)

def lambda_handler(event, context):
    try:
        # Parse S3 Event Notification
        for record in event['Records']:
            s3_bucket = record['s3']['bucket']['name']
            s3_object_key = record['s3']['object']['key']
            
            # Download file from AWS S3
            temp_file = f"/tmp/{s3_object_key.split('/')[-1]}"
            s3_client.download_file(s3_bucket, s3_object_key, temp_file)

            # Upload file to MinIO
            minio_client.fput_object(MINIO_BUCKET, s3_object_key, temp_file)

            print(f"Successfully replicated {s3_object_key} to MinIO")

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Replication Failed')
        }

    return {
        'statusCode': 200,
        'body': json.dumps('Replication Successful')
    }
