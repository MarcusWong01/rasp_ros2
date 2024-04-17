import socket
import requests
import cv2
import json
import base64

def setup_socket():
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
    socket_address = ('localhost', 9999)
    server_socket.bind(socket_address)
    return server_socket, socket_address

def sender_socket(server_socket, socket_address, frame):
    try:
        encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        message = base64.b64encode(buffer)
        server_socket.sendto(message, socket_address)
    except Exception as e:
        print(f"Error in sender_socket: {e}")

def jsonSender_socket(server_socket, socket_address, bboxes):
    try:
        bboxes_json = json.dumps(bboxes)
        encoded_message = base64.b64encode(bboxes_json.encode('utf-8'))
        # Send encoded message over socket
        server_socket.sendto(encoded_message, socket_address)
    except Exception as e:
        print(f"Error in jsonSender_socket: {e}")

def jsonSender_HTTPPost(bboxes):
    if bboxes is not None:
        json_data = json.dumps(bboxes)

        # Send HTTP POST request to the .NET C# project
        url = 'http://localhost:8080/'
        headers = {'Content-Type': 'application/json'}
        print("Sending HTTP POST request to:", url)
        print("JSON data:", json_data)
        response = requests.post(url, data=json_data, headers=headers)

        # Check response status
        if response.status_code == 200:
            print("Data sent successfully")
        else:
            print("Failed to send data")
def close_socket(server_socket):
    server_socket.close()




