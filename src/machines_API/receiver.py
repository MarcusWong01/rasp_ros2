import socket
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

def receive_image_process():
    # Connect to the server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
    server_socket.bind(('0.0.0.0', 1936))

    model = Yolo.load_mode()

    try:
        while True:
            # Receive and display the image
            footage = receive_image(server_socket)
            results = Yolo.detect(model, footage)
            Yolo.getInfo(results, footage)
    finally:
        # Close the connection
        server_socket.close()
