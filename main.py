# Dict to quickly locate nodes
# ----------------------------
node_tracker = {}

# File handling to read the input file
# ------------------------------------
connections = []
with open("input.txt") as f:
    content = f.readlines()
for line in content:
    line = line.strip()
    parts = map(int, line.split(","))
    connections.append(parts)
print connections


# A node in the object graph
# --------------------------
class Node(object):
    def __init__(self, val):
        self.children = []
        self.parent = None
        self.val = val

    def add_child(self, child):
        self.children.append(child)
        
    def set_parent(self, parent):
        self.parent = parent


# Build up the object graph
# -------------------------
for connection in connections:
    child_value = connection[0]
    parent_value = connection[1]
    child_node = Node(child_value)
    if parent_value in node_tracker:
        parent_node = node_tracker[parent_value]
    else:
        parent_node = Node(parent_value)
        node_tracker[parent_value] = parent_node
    parent_node.add_child(child_node)
    child_node.set_parent(parent_node)
    node_tracker[child_value] = child_node


# Starting from the leaf nodes, traverse up and return a list
# -----------------------------------------------------------
def traverse_up(tracker, some_value):
    ancestry = []
    if some_value in tracker:
        current_node = tracker[some_value]
        while True:
            ancestry.append(current_node.val)
            if not current_node.parent:
                break
            else:
                current_node = current_node.parent
    return ancestry


# Build up the linages list with full linages starting with ancestor
# nodes down to the leaf nodes
def express_linage(tracker, node, linages):
    if len(node.children):
        for child_node in node.children:
            express_linage(tracker, child_node, linages)
    else:
        up = traverse_up(tracker, node.val)
        up.reverse()
        linages.append(up)


# Starting from any top level parent node, return all pathways going
# down to leaves
# --------------------------------------------------------------------
def traverse_down(tracker, some_value):
    linages = []
    if some_value in tracker:
        express_linage(tracker, tracker[some_value], linages)
    return linages


# Test assertions
# ---------------
assert traverse_up(node_tracker, 7) == [7, 5, 25]
assert traverse_up(node_tracker, 5) == [5, 25]
assert traverse_up(node_tracker, 4) == [4, 25]
assert traverse_up(node_tracker, 100) == []
assert traverse_down(node_tracker, 3) == [[3, 8]]
assert traverse_down(node_tracker, 25) == [[25, 5, 7], [25, 4, 2]]
