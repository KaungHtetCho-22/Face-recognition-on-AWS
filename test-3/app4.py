from flask import Flask, render_template, jsonify, request
import boto3
import io
from PIL import Image

app = Flask(__name__)

# Initialize AWS clients
rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

# Route to display webcam feed and recognize faces
@app.route('/')
def index():
    ec2_url = 'http://35.153.140.177:8080'  # Replace with your EC2 instance's public IP or DNS
    return render_template('index3.html', ec2_url=ec2_url)

# Route to process captured image and perform facial recognition
@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'No image uploaded'})

    image_file = request.files['image']
    image_bytes = image_file.read()

    # Use AWS Rekognition to search for faces in the image
    response = rekognition.search_faces_by_image(
        CollectionId='testCollection',
        Image={'Bytes': image_bytes}
    )

    found = False
    for match in response.get('FaceMatches', []):
        print(match['Face']['FaceId'], match['Face']['Confidence'])
        face = dynamodb.get_item(
            TableName='testTable',
            Key={'RekognitionId': {'S': match['Face']['FaceId']}}
        )
        if 'Item' in face:
            print("Found Person: ", face['Item']['FullName']['S'])
            found = True
            return jsonify({'status': 'recognized', 'name': face['Item']['FullName']['S']})

    if not found:
        print("Person cannot be recognized")
        return jsonify({'status': 'not_recognized'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)