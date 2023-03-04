import socket
import sys

server_host = sys.argv[1]
server_port = int(sys.argv[2])
file_name = sys.argv[3]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_host, server_port))

request = f"GET /{file_name} HTTP/1.1\r\nHost: {server_host}:{server_port}\r\n\r\n" 
sock.sendall(request.encode())

BUFFER_SIZE = 2048
response = sock.recv(BUFFER_SIZE)

if response.startswith(b"HTTP/1."):
    status_code = int(response.decode().split()[1])
    if status_code == 404:
        print(f"Error: {response.decode().splitlines()[0]}")
        sock.close()
        sys.exit(1)

file_content = response.decode().split('\r\n\r\n')[1]

print(file_content)

sock.close()
