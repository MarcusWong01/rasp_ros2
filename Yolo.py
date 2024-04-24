import sender
import cv2
import base64
import JsonFunction
from ultralytics import YOLO

def load_mode():
    model = YOLO('models/best1.pt')
    return model

def detect(model, frame):
    return model.predict(frame)

def getInfo(results, image):
    bboxes = []
    # Convert image to base64
    _, encoded_image = cv2.imencode('.jpg', image)
    base64_image = base64.b64encode(encoded_image).decode('utf-8')
    for result in results:
        boxes = result.boxes
        xyxys = boxes.xyxy  # Access bounding box coordinates in [x1, y1, x2, y2] format
        confidences = boxes.conf.tolist()  # Convert confidence scores to Python list
        class_labels = boxes.cls.tolist()  # Convert class labels to Python list
        for xyxy, confidence, class_label in zip(xyxys, confidences, class_labels):
            x1, y1, x2, y2 = xyxy.tolist()
            width = x2 - x1
            height = y2 - y1
            if confidence >= 0.5:
                bboxes.append({'image': base64_image,
                               'x1': x1,
                               'y1': y1,
                               'width': width,
                               'height': height,
                               'confidence': confidence,
                               'class_label': class_label})

                sender.jsonSender_HTTPPost(bboxes)
