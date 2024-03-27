import boto3

# Initialize AWS SDK clients
s3 = boto3.client('s3')
kms = boto3.client('kms')

# Define the KMS key ID for encryption
kms_key_id = 'ef00b30e-65c4-4fc4-ba48-d6f85c4636b0'

# Get list of objects for indexing
images = [
    # ('image1.jpg', 'Allison Becker'),
    # ('image2.jpg', 'Andy Robertson'),
    # ('image3.jpg', 'Mac Allister'),
    # ('image4.jpg', 'Mohamad Salah'),
    # ('image5.jpg', 'Trent Arnold'),
    # ('image6.jpg', 'Van Dijki'),
    # ('image7.jpg', 'Minn Banya'),
    # ('image8.jpg', 'Min Thet'),
    # ('image9.jpg', 'Poe Poe'),
    # ('image10.jpg', 'Kaung Htet Cho'),
    # ('image11.jpg', 'Kaung Htet Cho'),
    # ('image12.jpg', 'Kaung Htet Cho'),
    # ('image13.jpg', 'Kaung Htet Cho'),
    # ('image14.jpg', 'Win Phyo'),
    # ('image15.jpg', 'Phone Myint Zaw'),
    # ('image16.jpg', 'Boss'),
    ('image17.jpg', 'Aung Myat Thu')
]

# Iterate through list to upload objects to S3
for image in images:
    with open(image[0], 'rb') as file:
        image_data = file.read()

    # Encrypt the image data using AWS KMS
    response = kms.encrypt(
        KeyId=kms_key_id,
        Plaintext=image_data
    )
    encrypted_image_data = response['CiphertextBlob']

    # Upload the encrypted image data to S3
    s3.put_object(
        Bucket='kaung-test-bucket',
        Key='index/' + image[0],
        Body=encrypted_image_data,
        Metadata={'FullName': image[1]}
    )
