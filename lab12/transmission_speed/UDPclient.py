from clientGUI import ClientGUI
import socket
import tkinter as tk

class ClientUDP(ClientGUI):
    def __init__(self, root):
        super().__init__(root, 'UDP')

    def send_data(self):
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        num_packets = int(self.packets_entry.get())

        udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_address = (ip, int(port))

        for _ in range(num_packets):
            data_size = 1024 
            data = self.generate_data_with_timestamp(data_size)
            udp_client_socket.sendto(data.encode(), udp_address)
        
        udp_client_socket.close()

        
if __name__ == "__main__":
    root = tk.Tk()
    app = ClientUDP(root)
    root.mainloop()