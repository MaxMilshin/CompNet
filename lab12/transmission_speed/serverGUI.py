import tkinter as tk

class ServerGUI:
    def __init__(self, root, protocol_name):
        self.root = root
        self.root.title(f"{protocol_name} Server")
        self.root.geometry("300x250")

        self.ip_label = tk.Label(root, text="Sender IP Address:")
        self.ip_label.pack()
        self.ip_entry = tk.Entry(root)
        self.ip_entry.pack()

        self.port_label = tk.Label(root, text="Receiver Port:")
        self.port_label.pack()
        self.port_entry = tk.Entry(root)
        self.port_entry.pack()

        self.start_button = tk.Button(root, text="Start", command=self.start_server)
        self.start_button.pack()

        self.data_label = tk.Label(root, text="Data Transfer Statistics")
        self.data_label.pack()

        self.speed_label = tk.Label(root, text="Speed: 0 bytes/second")
        self.speed_label.pack()

        self.received_label = tk.Label(root, text="Received Packets: 0")
        self.received_label.pack()

        self.lost_label = tk.Label(root, text="Lost Packets: 0")
        self.lost_label.pack()