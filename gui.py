from PyQt5 import QtWidgets  # import PyQt5 widgets and for creating the GUI
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # import Matplotlib canvas for plotting our graphs in the GUI
import matplotlib.pyplot as plt  # import for drawing the plots
import sys 
from algorithms import kruskal
from dataset import data  # import the data class for generating the graph data
import random  # import random for generating random weights and positions for the nodes
class MSTGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minimum Spanning Tree")
        self.layout = QtWidgets.QVBoxLayout(self)

        # input fields
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

        # plot
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # connecting buttons to their respective functions
        self.gen_button.clicked.connect(self.generate_graph)
        self.calc_button.clicked.connect(self.calculate_mst)

    def generate_graph(self):
        """
        Generate the graph data and plot it.
        """
        if not self.node_input.text() or not self.conn_input.text():
            QtWidgets.QMessageBox.warning(self, "Warning", "Please fill in all fields.")
            return

        # Clear previous graph data
        self.graph_data = None

        try:  # Properly indented under the method
            num_nodes = int(self.node_input.text())
            max_connections = int(self.conn_input.text())
            self.graph_data = data(num_nodes, max_connections)
            self.graph_data.generate()

            for node in self.graph_data.arrayOfNodes:
                print(f"Node {node.data} connections: {node.getConnections()}")

            # Clear the plot
            self.ax.clear()
            self.ax.set_title("Generated Graph")

            # Generate random positions for nodes
            node_positions = {}
            for node in self.graph_data.arrayOfNodes:
                x, y = random.uniform(0, 10), random.uniform(0, 10)  # Random 2D positions
                node_positions[node.data] = (x, y)
                self.ax.plot(x, y, 'o', label=f"Node {node.data}")  # Plot the node

            # Plot the edges
            for node in self.graph_data.arrayOfNodes:
                x1, y1 = node_positions[node.data]
                for connection, weight in node.getConnections():
                    x2, y2 = node_positions[connection.data]
                    self.ax.plot([x1, x2], [y1, y2], 'k-', alpha=0.5)  # Plot the edge
                    # Optionally, display the weight near the edge
                    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                    self.ax.text(mid_x, mid_y, str(weight), fontsize=8, color='blue')

            self.ax.legend(loc = "lower left")
            self.canvas.draw()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to generate graph: {e}")

    def calculate_mst(self):

        if not self.graph_data:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please first generate a graph.")
            return

        try:
            # Debug: Print the graph data
            print("Graph Nodes and Edges:")
            for node in self.graph_data.arrayOfNodes:
                print(f"Node {node.data} connections: {node.getConnections()}")

            # Calculate the MST using Kruskal's algorithm
            mst = kruskal(self.graph_data)

            print("MST:", mst)

            # Clear the plot
            self.ax.clear()
            self.ax.set_title("Minimum Spanning Tree")

            # Generate random positions for nodes (reuse from generate_graph)
            node_positions = {}
            for node in self.graph_data.arrayOfNodes:
                x, y = random.uniform(0, 10), random.uniform(0, 10)  # Random 2D positions
                node_positions[node.data] = (x, y)
                self.ax.plot(x, y, 'o', label=f"Node {node.data}")  # Plot the node

            # Plot the MST edges
            for edge in mst:
                start_node, end_node, weight = edge
                x1, y1 = node_positions[start_node]
                x2, y2 = node_positions[end_node]
                self.ax.plot([x1, x2], [y1, y2], 'g-', label=f"Edge {start_node}-{end_node} (Weight: {weight})")  # MST edge

            # Add legend
            self.ax.legend(loc = "lower left")
            self.canvas.draw()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to calculate MST: {e}")