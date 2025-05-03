""""
what does a server do?
1. Create a socket 
2. Bind the socket to ip and port
3. listen for incoming requests
4. accept the requests from client
5. receive the data
6. send back the data
7. close server and client connections
"""
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(("0.0.0.0", 12349))
server_socket.listen()
client_socket , client_address = server_socket.accept()
while True:
    data = client_socket.recv(1024)
    print(f"Client: {data.decode()}")
    client_socket.sendall(input().encode())
else:
    client_socket.close()
    server_socket.close()