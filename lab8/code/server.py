import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
CLIENT_UDP_PORT = None
BUFFER_SIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((UDP_IP, UDP_PORT))

expected_seqnum = 0

def send_file_to_client():
    seqnum = 0
    FILENAME = 'server_file_to_send.txt'
    TIMEOUT = 0.01
    with open(FILENAME, 'rb') as f:
        data = f.read(BUFFER_SIZE-1)
        while data:
            packet = seqnum.to_bytes(1, byteorder='big') + data
            server_socket.sendto(packet, (UDP_IP, CLIENT_UDP_PORT))
            server_socket.settimeout(TIMEOUT)
            try:
                ack, addr = server_socket.recvfrom(BUFFER_SIZE)
                if ack[0] == seqnum:
                    seqnum = 1 - seqnum
                    data = f.read(BUFFER_SIZE-1)
            except socket.timeout:
                print(f"Timeout after {TIMEOUT} seconds")
            except Exception as e:
                print(f"Error: {e}")
                break
    server_socket.sendto(b'EOF', (UDP_IP, CLIENT_UDP_PORT))




while True:
    try:
        data, addr = server_socket.recvfrom(BUFFER_SIZE)
        CLIENT_UDP_PORT = addr[1]
        if data == b'EOF':
            #switch on sending mode
            send_file_to_client()
            server_socket.settimeout(None)
            continue
        seqnum = int.from_bytes(data[:1], byteorder='big')
        if seqnum == expected_seqnum:
            message = data[1:]
            server_socket.sendto(seqnum.to_bytes(1, byteorder='big') + b'ACK', addr)
            expected_seqnum = 1 - expected_seqnum
            if not message:
                break
            with open('received_file', 'ab') as f:
                f.write(message)
        else:
            server_socket.sendto((1 - expected_seqnum).to_bytes(1, byteorder='big') + b'ACK', addr)
    except Exception as e:
        print(f"Error: {e}")
        break

server_socket.close()
