from flask import Flask, render_template, jsonify, request
import boto3
import cv2
import numpy as np
import base64

app = Flask(__name__)

# Initialize AWS clients
rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    image_data = request.form['image_data']
    encoded_image = image_data.split(",")[1]

    try:
        nparr = np.frombuffer(base64.b64decode(encoded_image), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        _, image_bytes = cv2.imencode('.jpg', frame)

        response = rekognition.search_faces_by_image(
            CollectionId='testCollection',
            Image={'Bytes': image_bytes.tobytes()}
        )

        found = False
        for match in response.get('FaceMatches', []):
            face = dynamodb.get_item(
                TableName='testTable',
                Key={'RekognitionId': {'S': match['Face']['FaceId']}}
            )
            if 'Item' in face:
                found = True
                return jsonify({'status': 'recognized', 'name': face['Item']['FullName']['S']})

        if not found:
            return jsonify({'status': 'not_recognized'})

    except Exception as e:
        print("Error processing image:", str(e))
        return jsonify({'status': 'error', 'message': 'Failed to process image'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)