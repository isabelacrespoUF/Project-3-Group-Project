from PyQt5 import QtWidgets  # importing PyQt5 widgets and for creating the GUI
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # importing Matplotlib canvas for plotting our graphs in the GUI
import matplotlib.pyplot as plt  # importing for drawing the plots
from algorithms import kruskal # importing kruskal's algorithm for calculating the minimum spanning tree
from dataset import data  # importing the data class for generating the graph data
import random  # importing random for generating random weights and positions for the nodes
class MSTGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # setting up gui window and title
        self.setWindowTitle("Minimum Spanning Tree Generator")
        self.layout = QtWidgets.QVBoxLayout(self)

        # input fields in the gui
        self.node_input = QtWidgets.QLineEdit("")
        self.conn_input = QtWidgets.QLineEdit("")
        self.layout.addWidget(QtWidgets.QLabel("Number of Nodes:"))
        self.layout.addWidget(self.node_input)
        self.layout.addWidget(QtWidgets.QLabel("Max Number of Connections:"))
        self.layout.addWidget(self.conn_input)

        # button setp for generating the graph and calculating our mst
        self.gen_button = QtWidgets.QPushButton("Generate Your Graph")
        self.calc_button = QtWidgets.QPushButton("Calculate MST")
        self.layout.addWidget(self.gen_button)
        self.layout.addWidget(self.calc_button)

        # plotting area
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # connecting buttons to their respective functions
        self.gen_button.clicked.connect(self.generate_graph)
        self.calc_button.clicked.connect(self.calculate_mst)

    def generate_graph(self): # function to generate the graph based on user input
    
        if not self.node_input.text() or not self.conn_input.text():    # checks if user input is empty
            QtWidgets.QMessageBox.warning(self, "Warning", "Please fill in all fields.")
            return

        self.graph_data = None # clearing the previous graph data

        try: # obtaining the user input for the number of nodes and max connections
            num_nodes = int(self.node_input.text())
            max_connections = int(self.conn_input.text())
            self.graph_data = data(num_nodes, max_connections)
            self.graph_data.generate() # generating the graph data using the data class

            for node in self.graph_data.arrayOfNodes: # code debug statement forprinting the nodes and their connections
                print(f"Node {node.data} connections: {node.getConnections()}")

            self.ax.clear()  # clearing our previous plot once the button is pressed to generate new data
            self.ax.set_title("Generated Graph")

            node_positions = {}
            for node in self.graph_data.arrayOfNodes:
                x, y = random.uniform(0, 10), random.uniform(0, 10)  # using import random we can generate random positions for the nodes
                                                                    # this prevents nodes from printing directly on to the x axis solely       
                node_positions[node.data] = (x, y)
                self.ax.plot(x, y, 'o', label=f"Node {node.data}")  # plots our nodes

            for node in self.graph_data.arrayOfNodes:
                x1, y1 = node_positions[node.data]
                for connection, weight in node.getConnections():
                    x2, y2 = node_positions[connection.data]
                    self.ax.plot([x1, x2], [y1, y2], 'k-', alpha=0.5)  # Plot the edge
                    # Optionally, display the weight near the edge
                    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                    self.ax.text(mid_x, mid_y, str(weight), fontsize=8, color='blue')

            self.ax.legend(loc = "lower left")  # keeps legend in place
            self.canvas.draw() 

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to generate graph: {e}")

    def calculate_mst(self):

        if not self.graph_data:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please first generate a graph.")
            return

        try:
            print("Graph Nodes and Edges:")
            for node in self.graph_data.arrayOfNodes:
                print(f"Node {node.data} connections: {node.getConnections()}")

            mst = kruskal(self.graph_data) # calculating our mst using kruskal's algorithm

            print("MST:", mst) # code debug statement for our mst

            self.ax.clear()
            self.ax.set_title("Minimum Spanning Tree")

            
            node_positions = {}
            for node in self.graph_data.arrayOfNodes:
                x, y = random.uniform(0, 10), random.uniform(0, 10)  # generating random positions for nodes as we did in the generate_graph function
                node_positions[node.data] = (x, y)
                self.ax.plot(x, y, 'o', label=f"Node {node.data}")  

            for edge in mst: # iterating through our mst to plot the edges and their weights
                start_node, end_node, weight = edge 
                x1, y1 = node_positions[start_node] 
                x2, y2 = node_positions[end_node] 
                self.ax.plot([x1, x2], [y1, y2], 'g-', label=f"Edge {start_node}-{end_node} (Weight: {weight})")  # MST edge

            self.ax.legend(loc = "lower left") # keeps legend in place
            self.canvas.draw()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to calculate MST: {e}")