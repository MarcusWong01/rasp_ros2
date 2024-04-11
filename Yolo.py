import base64
from ultralytics import YOLO

def load_mode():
    model = YOLO('models/best.pt')

def predict(model, frame):
    return model.predict(frame)

def getInfo(results, frame):
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
            bboxes.append({'frame': base64.b64encode(frame).decode('utf-8'),'x1': x1, 'y1': y1, 'width': width, 'height': height, 'confidence': confidence,
                           'class_label': class_label})
    return bboxes