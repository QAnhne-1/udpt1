import hashlib

class Node:
    def __init__(self, id, network):
        self.id = id
        self.network = network
        self.successor = self
        self.predecessor = self
        self.finger_table = {}
        self.keys = {}

    def find_successor(self, key):
        if self.id < key <= self.successor.id or (self.id > self.successor.id and (key > self.id or key <= self.successor.id)):
            return self.successor
        else:
            closest_preceding_node = self.find_closest_preceding_node(key)
            if closest_preceding_node == self:
                return self.successor
            return closest_preceding_node.find_successor(key)

    def find_closest_preceding_node(self, key):
        for i in sorted(self.finger_table.keys(), reverse=True):
            finger_id = self.finger_table[i].id
            if (self.id < finger_id < key) or (self.id > key and (finger_id > self.id or finger_id < key)):
                return self.finger_table[i]
        return self

    def join(self, start_node):
        if start_node:
            self.successor = start_node.find_successor(self.id)
            self.predecessor = self.successor.predecessor
            if self.predecessor:
                self.predecessor.successor = self
            self.successor.predecessor = self
        else:
            self.successor = self
            self.predecessor = self

    def stabilize(self):
        x = self.successor.predecessor
        if x and (self.id < x.id < self.successor.id or (self.id > self.successor.id and (x.id > self.id or x.id < self.successor.id))):
            self.successor = x
            self.successor.predecessor = self

    def fix_fingers(self, m):
        for i in range(1, m + 1):
            finger_id = (self.id + 2**(i-1)) % (2**m)
            self.finger_table[i] = self.find_successor(finger_id)

    def put(self, key, value):
        key_hash = int(hashlib.sha1(str(key).encode('utf-8')).hexdigest(), 16) % (2**self.network.m)
        target_node = self.find_successor(key_hash)
        target_node.keys[key_hash] = value
        print(f"Key '{key}' with hash {key_hash} stored at node {target_node.id}")

    def get(self, key):
        key_hash = int(hashlib.sha1(str(key).encode('utf-8')).hexdigest(), 16) % (2**self.network.m)
        target_node = self.find_successor(key_hash)
        if key_hash in target_node.keys:
            return target_node.keys[key_hash]
        return None

class ChordNetwork:
    def __init__(self, m):
        self.m = m
        self.nodes = {}

    def add_node(self, node_id):
        node = Node(node_id, self)
        if not self.nodes:
            node.join(None)
        else:
            start_node = list(self.nodes.values())[0]
            node.join(start_node)
        self.nodes[node_id] = node
        
    def get_node(self, node_id):
        return self.nodes.get(node_id)

    def show_network_status(self):
        print("\n--- Network Status ---")
        sorted_nodes = sorted(self.nodes.values(), key=lambda n: n.id)
        for node in sorted_nodes:
            print(f"\nNode ID: {node.id}")
            print(f"  Successor: {node.successor.id}")
            print(f"  Predecessor: {node.predecessor.id}")
            print("  Finger Table:")
            for i, finger_node in node.finger_table.items():
                print(f"    - Finger[{i}]: {finger_node.id}")

def hash_key(key, m):
    return int(hashlib.sha1(str(key).encode('utf-8')).hexdigest(), 16) % (2**m)

# Test cases
if __name__ == "__main__":
    m = 8
    chord_network = ChordNetwork(m=m)
    chord_network.add_node(10)
    chord_network.add_node(50)
    chord_network.add_node(150)
    chord_network.add_node(200)

    for node in chord_network.nodes.values():
        node.stabilize()
        node.fix_fingers(m)

    chord_network.show_network_status()

    print("\n--- Testing Data Storage and Retrieval ---")

    node_10 = chord_network.get_node(10)
    
    key_1 = "Tên tôi là An"
    key_1_hash = hash_key(key_1, m)
    print(f"Hashed ID for '{key_1}': {key_1_hash}")
    node_10.put(key_1, "An Nguyen")
    retrieved_val_1 = node_10.get(key_1)
    print(f"Retrieved value for '{key_1}': {retrieved_val_1}")

    key_2 = "Chord là gì"
    key_2_hash = hash_key(key_2, m)
    print(f"Hashed ID for '{key_2}': {key_2_hash}")
    node_10.put(key_2, "Hệ thống DHT")
    retrieved_val_2 = node_10.get(key_2)
    print(f"Retrieved value for '{key_2}': {retrieved_val_2}")