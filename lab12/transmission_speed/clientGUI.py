import random
import time
import tkinter as tk

class ClientGUI:
    def __init__(self, root, protocol_name):
        self.root = root
        self.root.title(f"{protocol_name} Client")
        self.root.geometry("300x200")

        self.ip_label = tk.Label(root, text="IP Address:")
        self.ip_label.pack()
        self.ip_entry = tk.Entry(root)
        self.ip_entry.pack()

        self.port_label = tk.Label(root, text="Port:")
        self.port_label.pack()
        self.port_entry = tk.Entry(root)
        self.port_entry.pack()

        self.packets_label = tk.Label(root, text="Number of Packets:")
        self.packets_label.pack()
        self.packets_entry = tk.Entry(root)
        self.packets_entry.pack()

        self.send_button = tk.Button(root, text="Send", command=self.send_data)
        self.send_button.pack()

    def generate_data_with_timestamp(self, size):
        timestamp = str(time.time())
        data = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=size - len(timestamp) - 1))
        return f"{timestamp} {data}"
