from scapy.all import ARP, Ether, srp

def get_network_devices(ip, mask):
    arp = ARP(pdst=ip+"/"+mask)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    
    result = srp(packet, timeout=3, verbose=0)[0]
    
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    
    return devices

ip = "192.168.0.102"
mask = "24"

devices = get_network_devices(ip, mask)

print("IP\t\t\tMAC Address")
for device in devices:
    print(f"{device['ip']}\t{device['mac']}")
