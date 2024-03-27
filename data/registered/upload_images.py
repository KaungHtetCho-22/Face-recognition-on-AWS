import boto3

s3 = boto3.resource('s3')

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
    #   ('image17.jpg', 'Aung Myat Thu'),
    #   ('image18.jpg', 'Lin Htun Naing'),
      ('image19.jpg', 'Myo Thiha')
]

# Iterate through list to upload objects to S3   
for image in images:
    file = open(image[0],'rb')
    object = s3.Object('kaung-test-bucket','index/'+ image[0])
    ret = object.put(Body=file,
                    Metadata={'FullName':image[1]})