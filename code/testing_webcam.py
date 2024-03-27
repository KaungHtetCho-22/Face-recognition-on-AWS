import boto3
import cv2
import io
from PIL import Image

# Initialize AWS clients
rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

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

    for match in response['FaceMatches']:
        print(match['Face']['FaceId'], match['Face']['Confidence'])

        face = dynamodb.get_item(
            TableName='testTable',
            Key={'RekognitionId': {'S': match['Face']['FaceId']}}
        )

        if 'Item' in face:
            print("Found Person: ", face['Item']['FullName']['S'])
            found = True

    if not found:
        print("Person cannot be recognized")

    # Display the frame
    cv2.imshow('Webcam', frame)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()