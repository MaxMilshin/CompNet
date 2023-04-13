import socket
import time
import statistics

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

packet_loss_count = 0
rtt_times = []
for i in range(1, 11):
    send_time = time.time()
    message = f'Ping {i} {send_time}'
    client_socket.sendto(message.encode(), ('localhost', 12000))
    
    try:
        client_socket.settimeout(1.0)
        response, server_address = client_socket.recvfrom(1024)
        receive_time = time.time()
        rtt = round((receive_time - send_time) * 1000, 2)
        rtt_times.append(rtt)
        print(f'Ping {i}: Response from {server_address[0]}: '
              f'time={rtt}ms')
    except socket.timeout:
        packet_loss_count += 1
        print(f'Ping {i}: Request timed out.')
    except Exception as e:
        print(f'Ping {i}: {e}')

PACKET_COUNT = 10

if rtt_times:
    min_rtt = min(rtt_times)
    max_rtt = max(rtt_times)
    avg_rtt = round(statistics.mean(rtt_times), 2)
    packet_loss_percent = round(packet_loss_count / PACKET_COUNT * 100, 2)
    print(f'\n--- Ping statistics ---')
    print(f'{PACKET_COUNT} packets transmitted, '
          f'{PACKET_COUNT - packet_loss_count} received, '
          f'{packet_loss_percent}% packet loss')
    print(f'min/avg/max = {min_rtt}/{avg_rtt}/{max_rtt} ms')
else:
    print(f'\n--- Ping statistics ---')
    print(f'{PACKET_COUNT} packets transmitted, '
          f'{PACKET_COUNT - packet_loss_count} received, '
          f'100.0% packet loss')
    print(f'min/avg/max = N/A/N/A/N/A')
