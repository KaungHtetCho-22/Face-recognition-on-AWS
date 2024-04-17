import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Cannot open camera")
    exit()

ret, frame = camera.read()

if not ret:
    print("Can't receive frame (stream end?). Exiting ...")
    exit()

cv2.imwrite('test_frame.jpg', frame)
print("Frame captured successfully")

camera.release()