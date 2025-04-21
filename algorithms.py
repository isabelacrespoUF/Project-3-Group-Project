import math


class CycleTracker:  # helps us find nodes that are together and avoid cycles for our MST (Minimum Spanning Tree)
    def __init__(self, nodes):
        self.parent = {}
        self.rank = {}
        for node in nodes:
            self.parent[node] = node  # initialize the parent of each node to itself
            self.rank[node] = 0

    def find(self, node):

        while self.parent[node] != node:  # finding the root out of the tree
            self.parent[node] = self.parent[self.parent[node]]  # flattening the tree to speed up our find operation
            node = self.parent[node]
        return node

    def union(self, node_1, node_2):  # connecting two sets of nodes and joining them into a group
        root_1 = self.find(node_1)  # we utilize rank to find the new tree parent
        root_2 = self.find(node_2)

        if root_1 != root_2:
            if self.rank[root_1] > self.rank[root_2]:
                self.parent[root_2] = root_1
            else:
                self.parent[root_1] = root_2
                if self.rank[root_1] == self.rank[root_2]:
                    self.rank[root_2] += 1
            #print(f"Union: {node_1} and {node_2}")  # code debug statement to check if the union is working accordingly
            return True
        #print(f"Cycle detected: {node_1} and {node_2}")  # code debug statement to check if the cycle is working accordingly as well
        # if the nodes are already connected, we return false to avoid cycles
        return False


def prim(spanTree):
    length = len(spanTree.arrayOfNodes)
    parent = -1
    minWeight = -1
    nodes = [False] * length
    nodes[0] = True
    Traversed = [spanTree.arrayOfNodes[0]]
    connections = []
    for i in range(length):
        minWeight = float('inf')
        for node in Traversed:
            for connection in node.getConnections():
                if nodes[connection[0].data]:
                    continue
                if connection[1] < minWeight:
                    minNode = connection[0]
                    parent = node.data
                    minWeight = connection[1]
        if minWeight == float('inf'):
            break
        nodes[minNode.data] = True
        connections.append((parent, minNode.data, minWeight))
        Traversed.append(minNode)
    sortMST = sorted(connections, key=lambda x: x[2])
    print(
        f"MST after Prim's algorithmn with a {len(spanTree.arrayOfNodes)} nodes and a max number of connections of {spanTree.maxConnects}:",
        sortMST)
    return sortMST


def kruskal(spanTree):  # kruskal's algorithm to find the minimum spanning tree

    graph_nodes = {node.data for node in spanTree.arrayOfNodes}  # extracting nodes from spantree object
    edges = []

    for node in spanTree.arrayOfNodes:
        for connection, weight in node.getConnections():  # going through each node and its connections to find the edges and their weights
            edges.append((node.data, connection.data, weight))  # appending the edges to a list

    #print("Printing all edges:", edges)  # code debug statement to check the edges and their weights

    edges.sort(key=lambda x: x[2])  # utilizing a lambda function in order to sort our edges by weight
    union_find = CycleTracker(graph_nodes)  # helper function to track our node connections
    tree_edges = []

    for u, v, weight in edges:  # going through each edge and checking if each node is connected without forming a cycle
        if union_find.union(u, v):
            tree_edges.append((u, v, weight))

    print(f"MST after Kruskal's algorithmn with a {len(spanTree.arrayOfNodes)} nodes and a max number of connections of {spanTree.maxConnects}:",
          tree_edges)  # code debug statement to check if kruska'ls algorithmn is working accordingly

    return tree_edges
