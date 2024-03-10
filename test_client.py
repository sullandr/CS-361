"""Simple client used to test miroservice"""

import socket
import json

HOST = "127.0.0.1"
PORT = 13000
COUNT = 5

# get user input and send to microservice, printing data sent and received
for i in range(COUNT):
    timezone = input("enter integer in range [-12 ... 14] or shortcode (PST, MST, etc.): ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))     # connect to socket server
        s.sendall(timezone.encode("utf-8"))     # send data
        data = s.recv(1024)     # receive response
        response = json.loads(data.decode("utf-8"))     # decode and unpack JSON data
        print(f"\nRequest: {timezone}")
        print(f"Received: {response}\n")
