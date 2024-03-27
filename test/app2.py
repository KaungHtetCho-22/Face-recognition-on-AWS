from flask import Flask, render_template, jsonify, request
import boto3
import cv2
import numpy as np
from PIL import Image
import base64
import io

app = Flask(__name__)

# Initialize AWS clients
rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

# Route to display webcam feed and recognize faces
@app.route('/')
def index():
    return render_template('index2.html')

# Route to process captured image and perform facial recognition
@app.route('/process_image', methods=['POST'])
def process_image():
    # Get image data from POST request
    data_url = request.json.get('image_data')

    # Remove header from base64 encoded image
    encoded_image = data_url.split(",")[1]
    # Decode base64 image and convert to OpenCV format
    nparr = np.frombuffer(base64.b64decode(encoded_image), np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert the frame to a PIL Image
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Convert the PIL Image to a byte stream
    stream = io.BytesIO()
    img.save(stream, format="JPEG")
    image_binary = stream.getvalue()

    # Use AWS Rekognition to search for faces in the frame
    response = rekognition.search_faces_by_image(
        CollectionId='testCollection',
        Image={'Bytes': image_binary}
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
