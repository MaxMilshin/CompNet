import random
import time
import queue

distances = {}
neighbors = {}
q = queue.Queue()
num_nodes = 4

def manage_edge(node1_id, node2_id, distance):
    node1_id, node2_id, distance
    if node1_id not in neighbors:
        neighbors[node1_id] = []
    if node2_id not in neighbors:
        neighbors[node2_id] = []
    if node2_id not in neighbors[node1_id]:
        neighbors[node1_id].append(node2_id)
    if node1_id not in neighbors[node2_id]:
        neighbors[node2_id].append(node1_id)
    distances[node1_id][node2_id] = distance
    distances[node2_id][node1_id] = distance

def initialize_network(graph):
    for edge in graph:
        u, v, w = edge
        manage_edge(u, v, w)
    
def send_packet(node_id, bad_neighbor_id):
    packet = distances[node_id]
    for neighbor_id in neighbors[node_id]:
        if neighbor_id != bad_neighbor_id:
            fl = receive_packet(neighbor_id, node_id, packet)
            if fl == True:
                q.put((neighbor_id, node_id))

def receive_packet(node_id, packet_sender_id, packet_distances):
    node_distances = distances[node_id]
    cost = node_distances[packet_sender_id]
    fl = False
    for neighbor_id in range(num_nodes):
        if node_distances[neighbor_id] > packet_distances[neighbor_id] + cost:
            node_distances[neighbor_id] = packet_distances[neighbor_id] + cost
            fl = True
    return fl
            
def get_neighbors(node_id, nodes):
    return nodes[node_id].neighbors

distances = {node_id: {dest_id: float('inf') for dest_id in range(num_nodes)} for node_id in range(num_nodes)}
for node_id in range(num_nodes):
    distances[node_id][node_id] = 0

initialize_network([(0, 1, 1), (0, 2, 3), (0, 3, 7), (1, 2, 1), (2, 3, 2)])


for node_id in range(num_nodes):
    q.put((node_id, None))

cnt = 0
while True:
    cnt += 1
    if cnt > 1:
        msg = f'''
Введите рёбра, которые хотите заменить в формате:
1 строка: m - количество ребер 
далее m строк вида: u v w, где (u, v) - двусторонее ребро и w - его вес
Или напишите 'exit()' чтобы завершить программу
'''
        print(msg)
        m = input()
        if m == 'exit()':
            exit(0)
        m = int(m)
        for i in range(m):
            u, v, w = list(map(int, input().split()))
            manage_edge(u, v, w)
            q.put((node_id, None))

    while not q.empty():
        node_id, bad_neighbor_id = q.get()
        send_packet(node_id, bad_neighbor_id)

    for node_id in range(num_nodes):
        print(f'Node {node_id}: {distances[node_id]}')
    
