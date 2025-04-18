import math


def prim(spanTree):
    """
    performs prims algorithm on a spanning Tree
    :param spanTree: needs a spanning tree
    :return: returns the connections needed to form a minimum spanning tree.
    The connections are returned in a 2D array. the second dimension format is as follows:
    [start node, end node, weight]

    """
    t = []
    connections = []
    nt = spanTree.arrayOfNodes.copy()
    t.append(spanTree.startNode)
    nt.pop(spanTree.indexOfStartNode)
    while len(nt) != 0:
        minNodeWeight = math.inf
        for i in t:
            for j, w in i.getConnections():
                if j not in t:
                    if w < minNodeWeight:
                        minNodeWeight = w
                        minNode = j
                        startNode = i
        t.append(minNode)
        nt.remove(minNode)
        connections.append([startNode.data, minNode.data, minNodeWeight])
    """
    #code to print out the weights between Nodes. format: [startNode, endNode, Weight]
    for i in range(len(spanTree.arrayOfNodes)):
        for j in spanTree.arrayOfNodes[i].getConnections():
            print(spanTree.arrayOfNodes[i].data, " ", j[0].data, " ", j[1])
        print()
    for i in connections:
        print(i)
    """
    return connections

def kruskal(spanTree):
    #FILL THIS OUT
    connections = []
    return connections
