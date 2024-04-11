import socket
import JsonFunction
import time
import cv2
import numpy as np
import base64
import sender
import Yolo

# Function to receive and decode image
def receive_image(receiver_socket):
    try:
        encoded_data, _ = receiver_socket.recvfrom(65536)  # Adjust buffer size as needed
        image_data = base64.b64decode(encoded_data)
        np_data = np.frombuffer(image_data, dtype=np.uint8)
        frame = cv2.imdecode(np_data, 1)
        # Check if received image is not empty
        if frame is not None and frame.size != 0:
            return frame
        else:
            print("Received empty image or decoding failed")
            return None
    except Exception as e:
        print("Error receiving image:", e)
        return None

def predict():
    # Connect to the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
    server_socket.bind(('0.0.0.0', 1935))

    model = Yolo.load_mode()
    outfile = JsonFunction.load_json()

    try:
        fps, st, frames_to_count, cnt = (0, 0, 30, 0)
        while True:
            # Receive and display the image
            footage = receive_image(server_socket)
            footage = cv2.putText(footage, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            results = model.predict(footage)

            if cnt == frames_to_count:
                try:
                    fps = round(frames_to_count / (time.time() - st))
                    st = time.time()
                    cnt = 0
                except:
                    pass
            cnt += 1

            results = Yolo.predict(model, footage)
            bboxes = Yolo.getInfo(results, footage)
            sender.sender_socket(bboxes)

            cv2.imshow('Received Image', footage)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if cv2.getWindowProperty('Received Image', cv2.WND_PROP_VISIBLE) < 1:
                break

        return footage
    finally:
        # Close the connection
        server_socket.close()
