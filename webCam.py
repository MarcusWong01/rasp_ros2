import cv2
import sender
import JsonFunction
import Yolo

def capture():
    # Initialize YOLO model
    model = Yolo.load_mode()

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
            results = Yolo.predict(model,frame)

            sender.sender_socket(frame)
            JsonFunction.writeJson(output_file, Yolo.getInfo(results))
            cv2.imshow('Received Image', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if cv2.getWindowProperty('Received Image', cv2.WND_PROP_VISIBLE) < 1:
                break
            return frame
    finally:
        cap.release()
