import boto3

# Create a KMS client
kms_client = boto3.client('kms')

# Define the AWS KMS Key ID
kms_key_id = '4f138ec0-dc5e-450c-bc1b-5a387084ad55'

# Create an S3 client
s3 = boto3.client('s3')

# Get list of objects for indexing
images = [
    ('image1.jpg', 'Allison Becker'),
    ('image2.jpg', 'Andy Robertson'),
    ('image3.jpg', 'Mac Allister'),
    # Add more images here
]

# Iterate through list to upload objects to S3   
for image in images:
    file_path = image[0]
    file_name = file_path.split('/')[-1]  # Extract file name from the file path
    
    # Open the file and read its content
    with open(file_path, 'rb') as file:
        image_data = file.read()
        
    # Encrypt the image data using KMS
    response = kms_client.encrypt(
        KeyId=kms_key_id,
        Plaintext=image_data
    )
    encrypted_image_data = response['CiphertextBlob']
    
    # Upload the encrypted image data to S3
    s3.put_object(
        Bucket='kaung-test-bucket',
        Key='index/' + file_name,
        Body=encrypted_image_data,
        Metadata={'FullName': image[1]}
    )



botocore.exceptions.ClientError: An error occurred (413) when calling the Encrypt operation: HTTP content length exceeded 200000 bytes.