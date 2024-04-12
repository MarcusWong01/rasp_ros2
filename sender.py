import socket
import cv2
import json
import base64

# Connect to the C# server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4096)
socket_address = ('localhost', 9999)
server_socket.bind(socket_address)

def sender_socket(frame):
    encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    message = base64.b64encode(buffer)
    server_socket.sendto(message, socket_address)

def jsonSender_socket(bboxes):
    # Convert bounding boxes data to JSON string
    bboxes_json = json.dumps(bboxes)
    # Encode JSON string
    encoded_message = base64.b64encode(bboxes_json.encode('utf-8'))
    # Send encoded message over socket
    server_socket.sendto(encoded_message, socket_address)