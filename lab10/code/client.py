import os
import sys
import struct
import socket
import select
import time

def calculate_checksum(packet):
    if len(packet) % 2 == 1:
        packet += b'\0'
    words = struct.unpack("!%sH" % (len(packet) // 2), packet)
    sum_ = sum(words)

    while sum_ >> 16:
        sum_ = (sum_ & 0xFFFF) + (sum_ >> 16)
    
    return ~sum_ & 0xFFFF

def ping(dest_addr, timeout=1, count=3):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', 64))

    dest_addr = socket.gethostbyname(dest_addr)

    sent_packets = 0
    received_packets = 0
    min_delay = float('inf')
    max_delay = float('-inf')
    total_delay = 0.0

    for i in range(count):
        icmp_id = os.getpid() & 0xFFFF
        icmp_seq = i

        packet = struct.pack("bbHHh", 8, 0, 0, icmp_id, icmp_seq) + b"Hello World!"
        checksum = calculate_checksum(packet)
        packet = struct.pack("bbHHh", 8, 0, socket.htons(checksum), icmp_id, icmp_seq) + b"Hello World!"

        try:
            send_time = time.time()

            sock.sendto(packet, (dest_addr, 1))

            sent_packets += 1

            ready = select.select([sock], [], [], timeout)
            if ready[0]:
                data, addr = sock.recvfrom(1024)

                recv_time = time.time()
                delay = (recv_time - send_time) * 1000

                icmp_type, icmp_code = struct.unpack("bb", data[20:22])

                if icmp_type == 0 and icmp_code == 0:
                    print("Ping to %s, seq=%d, delay=%.2f ms" % (dest_addr, icmp_seq, delay))
                    received_packets += 1
                    min_delay = min(min_delay, delay)
                    max_delay = max(max_delay, delay)
                    total_delay += delay
                else:
                    if icmp_type == 3 and icmp_code == 0:
                        print("Ping to %s, seq=%d, network unreachable" % (dest_addr, icmp_seq))
                    elif icmp_type == 3 and icmp_code == 1:
                        print("Ping to %s, seq=%d, host unreachable" % (dest_addr, icmp_seq))
                    else:
                        print("Ping to %s, seq=%d, error: icmp_type=%d, icmp_code=%d" % (dest_addr, icmp_seq, icmp_type, icmp_code))

            else:
                print("Ping to %s, seq=%d, timeout" % (dest_addr, icmp_seq))
        except socket.error as e:
            print("Ping to %s, seq=%d, error: %s" % (dest_addr, icmp_seq, e))

    sock.close()

    loss_percentage = ((sent_packets - received_packets) / sent_packets) * 100 if sent_packets > 0 else 0.0
    if received_packets > 0:
        avg_delay = total_delay / received_packets
        print("--- Ping statistics for %s ---" % dest_addr)
        print("%d packets transmitted, %d received, %.1f%% packet loss" % (sent_packets, received_packets, loss_percentage))
        print("round-trip min/avg/max = %.2f/%.2f/%.2f ms" % (min_delay, avg_delay, max_delay))
    else:
        print("No packets received.")

def main():
    args = sys.argv[1:]
    dest_addr = args[0]
    ping(dest_addr, count=10)
    
if __name__ == '__main__':
    main()