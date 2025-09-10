import hashlib

# Hàm băm ánh xạ giá trị vào không gian ID
def hash_id(value, m=4):
    return int(hashlib.sha1(value.encode()).hexdigest(), 16) % (2**m)

class Node:
    def __init__(self, node_id, m=4):
        self.id = node_id
        self.m = m
        self.successor = None
        self.finger_table = []

    def set_successor(self, successor):
        self.successor = successor

    def find_successor(self, key_id):
        # Nếu key nằm giữa nút hiện tại và successor
        if self.id < key_id <= self.successor.id:
            return self.successor
        # Nếu key nhỏ hơn tất cả, successor là nút nhỏ nhất
        if self.id > self.successor.id and (key_id > self.id or key_id <= self.successor.id):
            return self.successor
        # Nếu không, chuyển tiếp đến closest node trong finger table
        node = self.closest_preceding_node(key_id)
        if node == self:
            return self.successor
        return node.find_successor(key_id)

    def closest_preceding_node(self, key_id):
        for node in reversed(self.finger_table):
            if self.id < node.id < key_id:
                return node
        return self

# Xây dựng vòng Chord
nodes = [Node(i) for i in [1, 4, 8, 12]]
for i in range(len(nodes)):
    nodes[i].set_successor(nodes[(i+1) % len(nodes)])
    nodes[i].finger_table = nodes  # đơn giản: dùng tất cả nút làm finger table

# Thực hiện test cases
test_keys = [5, 4, 0]
for key in test_keys:
    start_node = nodes[0]
    successor = start_node.find_successor(key)
    print(f"Key {key} được lưu ở nút {successor.id}")
