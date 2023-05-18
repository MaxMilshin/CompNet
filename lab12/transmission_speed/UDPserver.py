from serverGUI import ServerGUI
import socket
import tkinter as tk
from tkinter import messagebox
import time

class ServerUDP(ServerGUI):
    def __init__(self, root):
        super().__init__(root, 'UDP')

    def start_server(self):
        receiver_ip = self.ip_entry.get()
        receiver_port = int(self.port_entry.get())

        udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        server_address = (receiver_ip, receiver_port)
        udp_server_socket.bind(server_address)

        
        total_packets = 0
        lost_packets = 0
        total_data_size = 0
        total_elapsed_time = 0

        while True:
            try:
                data, _ = udp_server_socket.recvfrom(1024)

                if data:
                    timestamp, received_data = data.decode().split(' ', 1)
                    total_data_size += len(received_data)
                    total_packets += 1

                    packet_time = float(timestamp)
                    elapsed_time = (time.time() - packet_time)
                    total_elapsed_time += elapsed_time
                    data_rate = total_data_size / 1024 / total_elapsed_time
                
                else:
                    lost_packets += 1

                self.speed_label.configure(text=f"Speed: {data_rate:.2f} Kb/S")
                self.speed_label.update()
                self.received_label.configure(text=f"Received Packets: {total_packets}")
                self.received_label.update()
                self.lost_label.configure(text=f"Lost Packets: {lost_packets}")
                self.lost_label.update()

            except socket.timeout:
                break

        udp_server_socket.close()

        messagebox.showinfo("Results", f"Total Packets: {total_packets}\nLost Packets: {lost_packets}\nData Rate: {data_rate} bytes/second")


if __name__ == "__main__":
    root = tk.Tk()
    app = ServerUDP(root)
    root.mainloop()
