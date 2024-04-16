import boto3
import json

# Create an S3 client
s3_client = boto3.client('s3')

# Define the KMS key ID
kms_key_id = 'e7c683e9-626e-4306-9a01-23ccf3230b9b'  

# Define the bucket name
bucket_name = 'kaunghtetcho-test-bucket'  

# Define the bucket policy
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::{}/*".format(bucket_name),
            "Condition": {"StringNotEquals": {"s3:x-amz-server-side-encryption": "aws:kms"}}
        }
    ]
}

# Convert the bucket policy to JSON string
bucket_policy_str = json.dumps(bucket_policy)

# Apply the bucket policy to the bucket
s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy_str)

# Enable SSE with KMS for the bucket
s3_client.put_bucket_encryption(
    Bucket=bucket_name,
    ServerSideEncryptionConfiguration={
        'Rules': [
            {
                'ApplyServerSideEncryptionByDefault': {
                    'SSEAlgorithm': 'aws:kms',
                    'KMSMasterKeyID': kms_key_id
                }
            }
        ]
    }
)

print("Bucket {} is now protected with KMS SSE.".format(bucket_name))
