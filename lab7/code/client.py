import time
import socket
from datetime import datetime

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)

for i in range(1, 11):
    message = f'Ping {i} {datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")}'
    start = time.time()
    client_socket.sendto(message.encode(), ('localhost', 12000))
    try:
        data, server = client_socket.recvfrom(1024)
        end = time.time()
        elapsed = end - start
        print(f'{data.decode()} RTT: {elapsed} seconds')
    except socket.timeout:
        print(f'Request {i} timed out')
client_socket.close()
