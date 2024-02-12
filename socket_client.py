#!/usr/bin/env python3

import socket

HOST = "127.0.0.1"  # server IP, can use server name as well, but using IP is better
PORT = 65432  # server port


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # establishing the socket from the device end
    s.connect((HOST, PORT)) #connects to the server IP and port
    s.sendall(b"A message from CS361") # sends the message in byte form to the server
    data = s.recv(1024) #receives the response from the server
    message = data.decode("utf-8")  #changes the data from byte datatype back to a string, so that 'b' can be removed.
    message.replace('b', '', 1)
print(f"Received {message!r} from server") #prints what is received back from the server

