import cv2
import sender
import Yolo
import base64

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
            results = Yolo.detect(model, frame)
            #image_bytes = base64.b64encode(frame.read())
            for result in results:
                boxes = result.boxes
                xyxys = boxes.xyxy  # Access bounding box coordinates in [x1, y1, x2, y2] format
                confidences = boxes.conf.tolist()  # Convert confidence scores to Python list
                class_labels = boxes.cls.tolist()  # Convert class labels to Python list
                for xyxy, confidence, class_label in zip(xyxys, confidences, class_labels):
                    x1, y1, x2, y2 = xyxy.tolist()
                    width = x2 - x1
                    height = y2 - y1
                    bboxes = [{
                               'x1': x1,
                               'y1': y1,
                               'width': width,
                               'height': height,
                               'confidence': confidence,
                               'class_label': class_label}]

                    sender.jsonSender_HTTPPost(bboxes)
    finally:
        cap.release()
