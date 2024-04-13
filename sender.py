import socket
import cv2
import base64

# Connect to the C# server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
socket_address = ('localhost', 9999)
server_socket.bind(socket_address)

def sender_socket(frame):
    encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    message = base64.b64encode(buffer)
    server_socket.sendto(message, socket_address)

def jsonSender_socket(bboxes):
    message = base64.b64encode(bboxes)
    server_socket.sendto(message, socket_address)


