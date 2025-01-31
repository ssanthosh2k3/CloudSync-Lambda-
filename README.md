# 🚀 AWS Lambda S3 to MinIO Replication

## 📌 Project Overview
This project implements an AWS Lambda function to replicate objects from an AWS S3 bucket to a MinIO storage system. It automatically synchronizes file uploads and deletions, ensuring data consistency across cloud storage solutions.

---

## 🎯 Use Cases
-  Automatic replication of new objects from AWS S3 to MinIO.
-  Synchronization of deletions across storage platforms.
-  Ensuring data availability in multiple storage backends.
-  Secure transfer of files with IAM roles and access keys.

---

## 🚀 Advantages
-  **Scalability:** Supports high-volume data replication.
-  **Automated Synchronization:** No manual intervention required.
-  **Fast & Efficient:** Uses AWS Lambda for real-time event-driven replication.
-  **Secure:** IAM policies ensure data protection.
-  **Easy Integration:** Works with AWS S3 and MinIO seamlessly.

---

## 🏗️ Architecture Setup
### 📝 Steps to Deploy
1️⃣ **Create a Lambda Function:**
   - Use AWS Lambda with runtime **Python 3.10**.

2️⃣ **Setup IAM Role:**
   - Attach an IAM role with **S3 Full Access** permissions.

3️⃣ **Inline Policy for S3 Permissions:**
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
                "arn:aws:s3:::s3_name/*",
                "arn:aws:s3:::s3_name"
            ]
        }
    ]
}
```

4️⃣ **Deploy Lambda Function:**
   - Install dependencies & package the function.

```sh
mkdir -p lambda_package
vim lambda_function.py  # Paste the function code
pip install minio -t lambda_package/
cd lambda_package
zip -r ../lambda_function.zip .
cd ..
zip -g lambda_function.zip lambda_function.py
```

5️⃣ **Upload & Deploy Lambda Function:**
   - Go to AWS Lambda dashboard, upload `lambda_function.zip`, and deploy.

6️⃣ **Configure S3 Event Notification:**
   - **Go to S3** → **Bucket** → **Properties** → **Create Event Notification**
   - Choose **Object Created** & **Object Removed**
   - Select destination as **Lambda Function** and attach your function.

---

## 📜 Lambda Function Code
```python
import json
import boto3
import os
from minio import Minio
from minio.error import S3Error

# AWS S3 Client
s3_client = boto3.client('s3')

# MinIO Client Configuration
MINIO_ENDPOINT = "objectstore.e2enetworks.net"  # ✅ Remove "https://"
MINIO_ACCESS_KEY = "your-key"
MINIO_SECRET_KEY = "your-key"
MINIO_BUCKET = "destination-bucket-name"

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=True  # Change to False if using HTTP
)

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            event_name = record['eventName']
            s3_bucket = record['s3']['bucket']['name']
            s3_object_key = record['s3']['object']['key']

            if event_name.startswith('ObjectCreated'):
                # Handle object creation: Copy the object to MinIO
                temp_file = f"/tmp/{s3_object_key.split('/')[-1]}"
                s3_client.download_file(s3_bucket, s3_object_key, temp_file)
                minio_client.fput_object(MINIO_BUCKET, s3_object_key, temp_file)
                print(f"Successfully replicated {s3_object_key} to MinIO")

            elif event_name.startswith('ObjectRemoved'):
                # Handle object deletion: Delete the object from MinIO
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

---

## 📌 Sample Test Event
To test the function manually, use this sample event:
```json
{
 "Records": [
   {
     "eventSource": "aws:s3",
     "eventName": "ObjectCreated:Put",
     "s3": {
       "bucket": {
         "name": "dr-k8s-velero"
       },
       "object": {
         "key": "python.pdf"
       }
     }
   }
 ]
}
```

---

## 🛠️ Tools Used
- ☁️ **AWS S3** - Cloud storage service
- 🏗️ **EOS** - Enterprise Object Store
- 🐍 **Python3** - Programming language
- 🔧 **MinIO Library** - For object storage operations

---

## 🔥 My Contribution
✅ **Designed & implemented** the entire architecture
✅ **Configured IAM roles** and security permissions
✅ **Set up AWS Lambda function** and S3 event triggers
✅ **Tested & deployed** the function for real-time synchronization

## Note: 
If you are going to perform bulk file transfer increase memeory and timeout in AWS Lambda

---

## 📢 Conclusion
This AWS Lambda function automates the replication of files from AWS S3 to MinIO, ensuring seamless synchronization and high availability. 🚀 If you find this helpful, feel free to ⭐ the project and contribute! Happy coding! 😃
