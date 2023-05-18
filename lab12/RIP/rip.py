import json
import threading
from multiprocessing import Manager

routers = {}
overall_completed = 0
updates_completed = {}
lock = threading.Lock()

class Router:
    def __init__(self, ip):
        self.ip = ip
        self.routing_table = {}
        self.neighbor_ips = []

    def update_routing_table(self, source_ip, table):
        any_updates = False
        with lock: 
            for destination, (cost, _) in table.items():
                if self.ip == destination:
                    continue
                if destination not in self.routing_table or self.routing_table[destination][0] > cost + 1:
                    self.routing_table[destination] = (cost + 1, source_ip)
                    any_updates = True
        return any_updates

    def simulate_rip_step(self):
        any_updates = False
        for neighbor_ip in self.neighbor_ips:
            neighbor_table = routers[neighbor_ip].routing_table
            if self.update_routing_table(neighbor_ip, neighbor_table):
                any_updates = True
        return any_updates

    def run(self):
        global overall_completed
        cnt = 0
        while True and cnt < 10000:
            cnt += 1
            new_value = not self.simulate_rip_step()
            prev_value = updates_completed[self.ip]
            if prev_value != new_value:
                with lock:  
                    if prev_value == True:
                        overall_completed -= 1
                    else:
                        overall_completed += 1
                    updates_completed[self.ip] = not prev_value
            with lock: 
                if overall_completed == len(routers):
                    return
            self.print_routing_table(pref=f'Simulation step {cnt}')

    def print_routing_table(self, pref='Final state'):
        text = f"""{pref} of router {self.ip} table:
[Source IP]\t[Destination IP]\t[Next Hop]\t[Metric]\n"""
        for destination, (cost, next_hop) in self.routing_table.items():
            text += f"{self.ip}\t{destination}\t\t{next_hop}\t{cost}\n"
        with lock:
            print(text)

def read_topology_from_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    for router_data in data:
        ip = router_data['ip']
        routers[ip] = Router(ip)
        updates_completed[ip] = False

    for router_data in data:
        ip = router_data['ip']
        neighbors = router_data['neigbours']
        for neighbor_ip in neighbors:
            routers[ip].routing_table[neighbor_ip] = (1, neighbor_ip)
            routers[ip].neighbor_ips.append(neighbor_ip)

def simulate_rip():
    threads = []
    for _, router in routers.items():
        thread = threading.Thread(target=router.run)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def main():
    filename = "topology.json" 
    read_topology_from_json(filename)
    simulate_rip()
    for _, router in routers.items():
        router.print_routing_table()

if __name__ == "__main__":
    main()
