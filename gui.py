from PyQt5 import QtWidgets  # import PyQt5 widgets and for creating the GUI
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # import Matplotlib canvas for plotting our graphs in the GUI
import matplotlib.pyplot as plt  # import for drawing the plots
import sys 

class CycleTracker: # helps us find nodes that are together and avoid cycles for our MST (Minimum Spanning Tree)
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes} # each node starts off by being their own parent with a rank of 0
        self.rank = {node: 0 for node in nodes}
    
    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node]) # reassignment to root node as path compression is required
        return self.parent[node] 

    def union(self, node_1, node_2):  # connecting two sets of nodes and joining them into a group
        root_1 = self.find(node_1)    # we utilize rank to find the new tree parent
        root_2 = self.find(node_2)

        if root_1 != root_2:
            if self.rank[root_1] > self.rank[root_2]:
                self.parent[root_2] = root_1
            else:
                self.parent[root_1] = root_2
                if self.rank[root_1] == self.rank[root_2]:
                    self.rank[root_2] += 1
            return True                   # we return true if the nodes were successfully connected and false otherwise due to a possible cycle
        return False
    
def kruskal(graph_nodes, edges): # Kruskal's algorithm to find the minimum spanning tree
        
        edges.sort(key = lambda x: x[2]) # utilizing a lambda function in order to sort our edges by weight
        union_find = CycleTracker({node.data for node in graph_nodes}) #helper function to track our node connections
        tree_edges = []

        for u,v, weight in edges: # going through each edge and checking if each node is connected and if not, we are able to join them
            if union_find(u,v):
                tree_edges.append((u,v, weight))
        
        return tree_edges

class MSTGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minimum Spanning Tree")
        self.layout = QtWidgets.QVBoxLayout(self)

        # Input fields
        self.node_input = QtWidgets.QLineEdit("")
        self.conn_input = QtWidgets.QLineEdit("")
        self.layout.addWidget(QtWidgets.QLabel("Number of Nodes:"))
        self.layout.addWidget(self.node_input)
        self.layout.addWidget(QtWidgets.QLabel("Max Number of Connections:"))
        self.layout.addWidget(self.conn_input)

        self.gen_button = QtWidgets.QPushButton("Generate Graph")
        self.calc_button = QtWidgets.QPushButton("Calculate MST")
        self.layout.addWidget(self.gen_button)
        self.layout.addWidget(self.calc_button)

        # Plot
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MSTGUI()
    window.show()
    sys.exit(app.exec_())