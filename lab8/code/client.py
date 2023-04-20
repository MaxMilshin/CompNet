import socket
import time

UDP_IP = "127.0.0.1"
SERVER_UDP_PORT = 5005
BUFFER_SIZE = 1024
FILENAME = 'file_to_send.txt'
TIMEOUT = 0.01

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

seqnum = 0

with open(FILENAME, 'rb') as f:
    data = f.read(BUFFER_SIZE-1)
    while data:
        packet = seqnum.to_bytes(1, byteorder='big') + data
        client_socket.sendto(packet, (UDP_IP, SERVER_UDP_PORT))
        client_socket.settimeout(TIMEOUT)
        try:
            ack, addr = client_socket.recvfrom(BUFFER_SIZE)
            if ack[0] == seqnum:
                seqnum = 1 - seqnum
                data = f.read(BUFFER_SIZE-1)
        except socket.timeout:
            print(f"Timeout after {TIMEOUT} seconds")
        except Exception as e:
            print(f"Error: {e}")
            break



# switch to receiving mode
client_socket.settimeout(None)
client_socket.sendto(b'EOF', (UDP_IP, SERVER_UDP_PORT))
expected_seqnum = 0
while True:
    try:
        data, addr = client_socket.recvfrom(BUFFER_SIZE)
        if data == b'EOF':
            break
        seqnum = int.from_bytes(data[:1], byteorder='big')
        if seqnum == expected_seqnum:
            message = data[1:]
            client_socket.sendto(seqnum.to_bytes(1, byteorder='big') + b'ACK', addr)
            expected_seqnum = 1 - expected_seqnum
            if not message:
                break
            with open('client_received_file', 'ab') as f:
                f.write(message)
        else:
            client_socket.sendto((1 - expected_seqnum).to_bytes(1, byteorder='big') + b'ACK', addr)
    except Exception as e:
        print(f"Error: {e}")
        break

client_socket.close()
