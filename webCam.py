import cv2
import sender
import JsonFunction
from ultralytics import YOLO

def capture():
    # Initialize YOLO model
    model = YOLO('models/best.pt')

    # Open JSON file in append mode
    output_file = JsonFunction.load_json()

    # Open the video capture device (webcam)
    cap = cv2.VideoCapture(0)  # Use 0 for default webcam, you can change it if needed
    try:
        while True:
            ret, frame = cap.read()  # Read frame from the webcam
            if not ret:
                break

            # Perform object detection using YOLO
            results = model.predict(frame)

            # Extract bounding box coordinates, confidence scores, and class labels
            bboxes = []
            for result in results:
                boxes = result.boxes
                xyxys = boxes.xyxy  # Access bounding box coordinates in [x1, y1, x2, y2] format
                confidences = boxes.conf.tolist()  # Convert confidence scores to Python list
                class_labels = boxes.cls.tolist()  # Convert class labels to Python list
                for xyxy, confidence, class_label in zip(xyxys, confidences, class_labels):
                    x1, y1, x2, y2 = xyxy.tolist()
                    width = x2 - x1
                    height = y2 - y1
                    bboxes.append({'x1': x1, 'y1': y1, 'width': width, 'height': height, 'confidence': confidence,
                                   'class_label': class_label})
            sender.sender_socket(frame)
            JsonFunction.writeJson(output_file, bboxes)
            cv2.imshow('Received Image', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if cv2.getWindowProperty('Received Image', cv2.WND_PROP_VISIBLE) < 1:
                break
            return frame
    finally:
        cap.release()
