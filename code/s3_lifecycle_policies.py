import boto3

# Create an S3 client
s3_client = boto3.client('s3')

# Define the bucket name
bucket_name = 'kaunghtetcho-test-bucket'  # Replace with your bucket name

# Define the lifecycle configuration
lifecycle_configuration = {
    'Rules': [
        {
            'ID': 'image-lifecycle-rule',
            'Prefix': 'images/',  # Replace with the prefix of your images
            'Status': 'Enabled',
            'Transitions': [
                {
                    'Days': 30,  # Transition to Standard-IA storage class after 30 days
                    'StorageClass': 'STANDARD_IA'
                },
                {
                    'Days': 365,  # Transition to Glacier storage class after 365 days
                    'StorageClass': 'GLACIER'
                }
            ],
            'Expiration': {
                'Days': 730  # Expire objects after 730 days (2 years)
            }
        }
    ]
}

# Configure the lifecycle policy for the bucket
s3_client.put_bucket_lifecycle_configuration(
    Bucket=bucket_name,
    LifecycleConfiguration=lifecycle_configuration
)

print("Lifecycle policy configured for bucket {}.".format(bucket_name))
