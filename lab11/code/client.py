import socket
import struct
import time

import random

def send_icmp_packet(dest_addr, ttl, packet_count=3):
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    icmp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    icmp_type = 8  
    icmp_code = 0  
    icmp_id = random.randint(0, 0xFFFF)  
    icmp_seq = random.randint(1, 0xFFFF)  
    icmp_data = b'Hello, World!' * 16  
    
    def calculate_checksum(data, k=16):
        sum = 0
        for i in range(0, len(data), k):
            num = int.from_bytes(data[i:i+k], byteorder='big', signed=False)
            sum += num
            sum = (sum & 0xffff) + (sum >> 16)
        checksum = ~sum & 0xffff
        return checksum
    
    icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, 0, icmp_id, icmp_seq)
    icmp_checksum = calculate_checksum(icmp_header + icmp_data)
    icmp_packet = struct.pack('!BBHHH32s', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq, icmp_data)

    
    for i in range(packet_count):
        send_time = time.time()
        icmp_socket.sendto(icmp_packet, (dest_addr, 0))
        icmp_socket.settimeout(1)
        try:
            recv_packet, addr = icmp_socket.recvfrom(1024)
            
            icmp_header = recv_packet[20:28]  
            icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq = struct.unpack('!BBHHH', icmp_header)
            
            recv_time = time.time()
        
        except socket.timeout:
            recv_time = None

        if recv_time:
            rtt = int((recv_time - send_time) * 1000)
            try:
                hostname = socket.gethostbyaddr(addr[0])[0]
            except:
                hostname = None
            yield (addr[0], hostname, rtt, icmp_type)
        else:
            yield None

    icmp_socket.close()

def trace_route(dest_addr, max_hops=30, packet_count=3):
    for ttl in range(1, max_hops+1):
        print(f'{ttl}:', end=' ')
        for res in send_icmp_packet(dest_addr, ttl, packet_count):
            if res:
                if res[1]:
                    print(f'{res[1]} ({res[0]} {res[2]}ms)', end=' ')
                else:
                    print(f'{res[0]} ({res[2]}ms)', end=' ')
                if res[3] == 0:
                    print('\nDestination host has reached!')
                    return 
            else:
                print('*', end=' ')
        print()

trace_route('akamai.com')
