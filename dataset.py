import random


class Node:
    """
    Structure which requires the value of the node and the max number of edges it could have.
    """

    def __init__(self, data, maxConnects):
        self.maxConnects = maxConnects
        if maxConnects < 4:
            raise "A node should have a maximum of at least four connections, otherwise it wouldn't intersect"
        self.connectedNodes = []
        self.data = data

    def addConnection(self, nextNode, weight):
        """
        Adds another node to the current one
        :param nextNode: The node which will be connected to the current one
        :param weight: the weight of the edge connecting the node
        """
        for i in self.connectedNodes:
            if i[0] == nextNode:
                return
        if nextNode == self:
            raise "Cannot do self loops"
        if len(self.connectedNodes) >= self.maxConnects:
            raise "Cannot add any more edges to the current Node"
        if len(nextNode.connectedNodes) >= nextNode.maxConnects:
            raise "Cannot add any more edges to the other Node"
        self.connectedNodes.append((nextNode, weight))
        nextNode.connectedNodes.append((self, weight))

    def addMultipleConnections(self, nextNodes, weights):
        """
        adds multiple connections to different nodes simultaneously
        :param nextNodes: (array) The nodes which will be connected
        :param weights: (array) The weights which will be in the respective edges connecting the nodes. Make sure that
        each edge corresponds to the respective node. For example nextNodes[0] will be connected to the current node
        with the value from weight[0].
        """
        if len(nextNodes) != len(weights):
            raise "Error: NextNodes and weights are not the same size"
        for i in range(len(nextNodes)):
            self.addConnection(nextNodes[i], weights[i])

    def getConnections(self):
        """
        Gets the nodes connecting to the current node with their weight
        :return value stored in a tuple. First value contains the node, second value
        contains the weight.
        """
        return self.connectedNodes

    def full(self):
        """
        Checks if a function has zero or one remaining connections
        :return: Boolean. True if yes. False if no.
        """
        if len(self.connectedNodes) == self.maxConnects:
            return True
        else:
            return False


class data:
    """
    Takes in the noNodes which will be in the dataset and the number of max connections each node will have.
    IMPORTANT: You will need to call the generate function to initialize the dataset.
    """

    def __init__(self, noNodes, maxConnects):
        self.arrayOfNodes = []
        self.noNodes = noNodes
        self.maxConnects = maxConnects
        self.weight = [i for i in range(noNodes * maxConnects)]
        for i in range(self.noNodes):
            self.arrayOfNodes.append(Node(i, self.maxConnects))
        self.indexOfStartNode = random.randrange(0, self.noNodes)
        self.startNode = self.arrayOfNodes[self.indexOfStartNode]

    def generate(self): #Generates the dataset
        completed = 1

        nt = self.arrayOfNodes.copy()
        t = []
        for i in range(len(self.arrayOfNodes)):
            total_connections = self.maxConnects - len(self.arrayOfNodes[i].getConnections())
            if total_connections != 0:
                nt.remove(self.arrayOfNodes[i])
            for j in range(total_connections):
                if len(nt) == 0:
                    break
                randomNode = random.randrange(0, len(nt))
                randomWeight = random.randrange(0, len(self.weight))

                self.arrayOfNodes[i].addConnection(nt[randomNode], self.weight[randomWeight])
                self.weight.pop(randomWeight)
                if nt[randomNode].full():
                    nt.pop(randomNode)

    def setStartNode(self, nodeIndex):
        """
        Sets one node to be the origin.
        :param nodeIndex: (int) access the nodeIndex element of arrayOfNodes
        """
        self.indexOfStartNode = nodeIndex
        self.startNode = self.arrayOfNodes[nodeIndex]

    def getStartNode(self):
        """
        returns the index of the starting node
        """
        return self.indexOfStartNode
