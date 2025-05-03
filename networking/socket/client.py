"""
what does a client do
1. Create a socket
2. connect to a server socket
3. send data
4. receive data
5. close connection
"""
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12349))
while True:
    client.sendall(input().encode())
    data = client.recv(1024)
    print("Server " +data.decode())
else:
    client.close()