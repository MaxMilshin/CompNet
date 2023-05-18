from clientGUI import ClientGUI
import socket
import tkinter as tk

class ClientTCP(ClientGUI):
    def __init__(self, root):
        super().__init__(root, 'TCP')

    def send_data(self):
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        num_packets = int(self.packets_entry.get())

        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_address = (ip, int(port))

        tcp_client_socket.connect(tcp_address)
        for _ in range(num_packets):
            data_size = 1024  
            data = self.generate_data_with_timestamp(data_size)
            tcp_client_socket.sendall(data.encode())
        
        tcp_client_socket.close()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = ClientTCP(root)
    root.mainloop()