# CloudSync Lambda - S3 to MinIO Replication

## Overview
This project automates the replication of objects between AWS S3 and EOS MinIO storage using an AWS Lambda function. The function listens for object creation and deletion events in an S3 bucket and ensures that the same operations are applied in MinIO storage.

## Project Use Cases
- **Backup & Disaster Recovery**: Automatically synchronize critical data from AWS S3 to EOS MinIO as a backup.
- **Multi-Cloud Storage Sync**: Enable seamless data replication between different cloud storage providers.
- **Data Processing & Archiving**: Replicate frequently accessed S3 data to MinIO for cost-effective storage solutions.
- **Hybrid Cloud Solutions**: Ensure real-time synchronization between AWS cloud storage and on-premise MinIO deployments.

## Advantages
- **Automation**: No manual intervention is required for synchronization.
- **Scalability**: Easily handles large volumes of data using AWS Lambda.
- **Cost-Effective**: Reduces AWS storage costs by offloading data to EOS MinIO.
- **Security**: AWS IAM roles and policies ensure secure access to S3.
- **Reliability**: Ensures consistency between storage solutions with automatic event-driven replication.

## Tools Used
- **AWS Lambda** (Python 3.10 runtime)
- **AWS S3** (Storage bucket for event triggers)
- **EOS MinIO** (Object storage for replication)
- **MinIO Python SDK**
- **Boto3** (AWS SDK for Python)
- **IAM Roles & Policies** (For AWS Lambda permissions)

## Setup Instructions

### Step 1: Create AWS Lambda Function
1. Go to AWS Lambda Dashboard.
2. Click **Create function** > Choose **Author from scratch**.
3. Enter a function name (e.g., `s3-to-minio-sync`).
4. Select **Runtime: Python 3.10**.
5. Choose an **Execution Role** with necessary permissions (explained in Step 2).
6. Click **Create function**.

### Step 2: Set Up IAM Role Permissions
Create an IAM Role with the following inline policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::your-s3-bucket/*",
        "arn:aws:s3:::your-s3-bucket"
      ]
    }
  ]
}
```

### Step 3: Prepare the Lambda Function Code
1. Create a local directory:
   ```sh
   mkdir -p lambda_package
   ```
2. Create a `lambda_function.py` file and paste the following code:

```python
import json
import boto3
from minio import Minio
from minio.error import S3Error

s3_client = boto3.client('s3')

# MinIO Configuration
MINIO_ENDPOINT = "objectstore.e2enetworks.net"
MINIO_ACCESS_KEY = "your-access-key"
MINIO_SECRET_KEY = "your-secret-key"
MINIO_BUCKET = "your-minio-bucket"

minio_client = Minio(
   MINIO_ENDPOINT,
   access_key=MINIO_ACCESS_KEY,
   secret_key=MINIO_SECRET_KEY,
   secure=True
)

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            event_name = record['eventName']
            s3_bucket = record['s3']['bucket']['name']
            s3_object_key = record['s3']['object']['key']

            if event_name.startswith('ObjectCreated'):
                temp_file = f"/tmp/{s3_object_key.split('/')[-1]}"
                s3_client.download_file(s3_bucket, s3_object_key, temp_file)
                minio_client.fput_object(MINIO_BUCKET, s3_object_key, temp_file)
                print(f"Successfully replicated {s3_object_key} to MinIO")

            elif event_name.startswith('ObjectRemoved'):
                minio_client.remove_object(MINIO_BUCKET, s3_object_key)
                print(f"Successfully deleted {s3_object_key} from MinIO")
    
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
```

### Step 4: Install Dependencies & Package the Code
```sh
pip install minio -t lambda_package/
cd lambda_package
zip -r ../lambda_function.zip .
cd ..
zip -g lambda_function.zip lambda_function.py
```

### Step 5: Upload & Deploy the Function
1. Go to AWS Lambda Dashboard.
2. Open the created function.
3. Click **Upload** and choose `lambda_function.zip`.
4. Click **Deploy**.

### Step 6: Test the Function
Create a test event with the following JSON data:

```json
{
  "Records": [
    {
      "eventSource": "aws:s3",
      "eventName": "ObjectCreated:Put",
      "s3": {
        "bucket": {
          "name": "your-s3-bucket"
        },
        "object": {
          "key": "test-file.txt"
        }
      }
    }
  ]
}
```

### Step 7: Configure S3 Event Notification
1. Open **S3 Dashboard** > Choose your bucket.
2. Click **Properties** > **Create Event Notification**.
3. Name it (e.g., `S3MinIOReplication`).
4. Choose **Object Created** and **Object Removed**.
5. Select **Lambda Function** as the destination.
6. Choose the deployed Lambda function.
7. Click **Save**.

## Future Enhancements
- Support for additional storage providers (Google Cloud Storage, Azure Blob Storage, etc.).
- Implement logging & monitoring using AWS CloudWatch.
- Add error handling & retry mechanism for failed transfers.
- Enhance security by using AWS Secrets Manager for credentials.

## My Contribution
- Architected and implemented the entire storage synchronization solution.
- Designed the event-driven pipeline using AWS Lambda and S3 triggers.
- Configured MinIO client and optimized storage replication workflows.
- Implemented IAM policies and security best practices.

## Conclusion
This solution automates S3-to-MinIO replication, ensuring seamless data synchronization, cost efficiency, and reliability. By leveraging AWS Lambda, event-driven triggers, and MinIO, this architecture provides a scalable and fault-tolerant approach to hybrid cloud storage management.

---

### 📌 **Maintained by:** [Santhosh](https://github.com/ssanthosh2k3)
