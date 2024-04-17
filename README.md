# Face recognition on AWS 
Cloud computing project from AIT

### About report 

- pdf >> final report
- Attached well-architected framework 
- Attached estimated cost calculated with aws pricing calculator 
- Attached demo-work


### How to setup this project

- Login into aws management console with root user
- Goes to cloudformation and create stack with cloudformation.yaml (don't forget to change settings according to your needs)
- After creating stack with .yaml, all services should be run right now
- Services attached to .yaml file
    - EC2 with security groups rules
    - DynamoDB as database
    - Rekognition for extract face indexes
    - Lambda to tigger s3 bucket, rekognition and dynamoDB (specific IAM role is attached)
    - S3 bucket with bucket permissions, lifecycle policies and KMS encryption
    - IAM Role with policies 
    - KMS (you have to generate customer-managed keys separately to attach)

### Workflow

- After stacking complete, you can upload images with upload_images.py in data/registered to S3 bucket
- As soon as the image uploading complete, it is ready to start 
- run app2.py in local_test

- As soon as the webpage loaded, open webcam and then ask the user to capture the image
- By using that captured image, model will looking for the matched data in aws dynamo db that stored registered images and names
- If the face is in database, it will shows up recognized
- Below sample screenshot webpage is running on the local and it works 

<img src='screenshot/local.png' alt="Step 1" width="600px" style="float: center" />
<figcaption> Web app running on local server </figcaption>
<br clear="left" />

###  Web app development

- Connect EC2 instance with SSH 
- All required necessary Userdata is bootstrapped in cloudformation.yaml (LINUX AMI)
- Git clone this repo in EC2 instance
- *You will need to import user's AWS ACCESS KEY ID and AWS SECRET ACCESS KEY into EC2 instance*
- Run the code/app/app.py for webhosting
- Access through <yourec2publicip>:8080

<img src='screenshot/image.png' alt="Step 1" width="600px" style="float: center" />
<figcaption> Web app running on EC2 instance server </figcaption>
<br clear="left" />


