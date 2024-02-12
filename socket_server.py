#!/usr/bin/env python3

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # listening port


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #creating the actual socket
    s.bind((HOST, PORT)) #binding the socket to the server address and assigning it to the port
    s.listen() #listens for connection requests
    conn, addr = s.accept() #conn is the incoming request, addr is that device's IP address
    with conn: # this opens the connection between server and incoming device
        print(f"Connected by {addr}")
        while True: #creates an infinite loop so that data transfer will be continuous
            data = conn.recv(1024) #this is receiving all of the data that is being sent
            if not data: #if data is no longer being received break the loop
                break
            message = data.decode("utf-8")
            message.replace('b', '', 1)
            conn.sendall(data) #sending data back as it is received in the loop.
    
    print(f"Received {message!r} from client")

    