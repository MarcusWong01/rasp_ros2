import cv2
import sender
import JsonFunction
import Yolo

def capture():
    # Initialize YOLO model
    model = Yolo.load_mode()

    # Open the video capture device (webcam)
    cap = cv2.VideoCapture(0)  # Use 0 for default webcam, you can change it if needed
    try:
        while True:
            ret, frame = cap.read()  # Read frame from the webcam
            if not ret:
                break

            # Perform object detection using YOLO
            results = Yolo.predict(model, frame)
            bboxes = Yolo.getInfo(results)
            sender.jsonSender_socket(bboxes)

        return frame
    finally:
        cap.release()