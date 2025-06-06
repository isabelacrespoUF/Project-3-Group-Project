from PyQt5 import QtWidgets  # importing PyQt5 widgets and for creating the GUI
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas  # importing Matplotlib canvas for plotting our graphs in the GUI
import matplotlib.pyplot as plt  # importing for drawing the plots
from matplotlib.transforms import Bbox  # import Bbox for scrollability
from algorithms import kruskal, prim  # importing kruskal's algorithm for calculating the minimum spanning tree
from dataset import data  # importing the data class for generating the graph data
import random  # importing random for generating random weights and positions for the nodes
import time


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

        # button set for generating the graph and calculating our mst
        self.gen_button = QtWidgets.QPushButton("Generate Your Graph")
        self.calc_buttonK = QtWidgets.QPushButton("Calculate MST With Kruskal's Algorithm")
        self.calc_buttonP = QtWidgets.QPushButton("Calculate MST With Prim's Algorithm")
        self.layout.addWidget(self.gen_button)
        self.layout.addWidget(self.calc_buttonK)
        self.layout.addWidget(self.calc_buttonP)

        # labels for displaying algorithm times
        self.prim_time_label = QtWidgets.QLabel("Prim's Algorithm Time: Not Calculated")
        self.kruskal_time_label = QtWidgets.QLabel("Kruskal's Algorithm Time: Not Calculated")
        self.layout.addWidget(self.prim_time_label)
        self.layout.addWidget(self.kruskal_time_label)

        # plotting area
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # textbox
        self.textBox = self.ax.text(0.05, 0.1, "")

        # connecting buttons to their respective functions
        self.gen_button.clicked.connect(self.generate_graph)
        self.calc_buttonK.clicked.connect(self.calculate_mstK)
        self.calc_buttonP.clicked.connect(self.calculate_mstP)

    def generate_graph(self):  # function to generate the graph based on user input

        if not self.node_input.text() or not self.conn_input.text():  # checks if user input is empty
            QtWidgets.QMessageBox.warning(self, "Warning", "Please fill in all fields.")
            return

        self.graph_data = None  # clearing the previous graph data

        try:  # obtaining the user input for the number of nodes and max connections
            num_nodes = int(self.node_input.text())
            max_connections = int(self.conn_input.text())

            if num_nodes > 1000:
                QtWidgets.QMessageBox.warning(self, "ERROR",
                                              "The maximum number of nodes that can be displayed is 1000. The output will be printed in the console")
                self.graph_data = data(num_nodes, max_connections)
                self.graph_data.generate()  # generating the graph data using the data class
                prim(self.graph_data)
                kruskal(self.graph_data)
                return
            if max_connections > num_nodes - 1:
                QtWidgets.QMessageBox.warning(self, "ERROR",
                                              "The maximum number of connections is greater than the number of nodes. Please enter a value below the number of nodes")
                return
            self.graph_data = data(num_nodes, max_connections)
            self.graph_data.generate()  # generating the graph data using the data class

            #for node in self.graph_data.arrayOfNodes:  # code debug statement forprinting the nodes and their connections
                #print(f"Node {node.data} connections: {node.getConnections()}")

            self.ax.clear()  # clearing our previous plot once the button is pressed to generate new data
            self.ax.set_title("Generated Graph")

            node_positions = {}
            for node in self.graph_data.arrayOfNodes:
                x, y = random.uniform(0, 10), random.uniform(0,
                                                             10)  # using import random we can generate random positions for the nodes
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
            leg = self.ax.legend(loc="upper right", bbox_to_anchor=(1.02, 0, 0.1, 1))
            self.prim_time_label.setText(f"Prim's Algorithmn Time: Not Calculated")
            self.kruskal_time_label.setText(f"Kruskal's Algorithmn Time: Not Calculated")
            def scroll_leg(evt):
                d = {"down": 100, "up": -100}
                if leg.contains(evt):
                    bbox = leg.get_bbox_to_anchor()
                    bbox = Bbox.from_bounds(bbox.x0, bbox.y0 + d[evt.button], bbox.width, bbox.height)
                    tr = leg.axes.transAxes.inverted()
                    leg.set_bbox_to_anchor(bbox.transformed(tr))
                    self.figure.canvas.draw_idle()

            self.figure.canvas.mpl_connect("scroll_event", scroll_leg)
            self.canvas.draw()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to generate graph: {e}")

    def display_graph_data(self):  # function to display the graph data in a new window if nodes exceed 1000
        if not self.graph_data:
            QtWidgets.QMessageBox.warning(self, "Warning", "No graph data to display.")
            return

        # creating a new window
        data_window = QtWidgets.QWidget()
        data_window.setWindowTitle("Graph Data")
        data_layout = QtWidgets.QVBoxLayout(data_window)

        data_text = QtWidgets.QTextEdit()
        data_text.setReadOnly(True)  # making the text box read-only

        graph_data_text = "Graph Nodes and Connections:\n"
        for node in self.graph_data.arrayOfNodes:  # iterating through the nodes and their connections
            connections = ", ".join([f"{conn.data} (Weight: {weight})" for conn, weight in
                                     node.getConnections()])  # getting the connections and their weights
            graph_data_text += f"Node {node.data}: {connections}\n"
        data_text.setText(graph_data_text)

        data_layout.addWidget(data_text)
        data_window.setLayout(data_layout)
        data_window.resize(800, 600)
        data_window.show()

    def calculate_mstK(self):
        self.figure.text
        if not self.graph_data:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please first generate a graph.")
            return

        try:
            startTime = time.time()
            mst = kruskal(self.graph_data)  # calculating our mst using kruskal's algorithm
            endTime = time.time()
            #print("MST:", mst)  # code debug statement for our mst

            self.ax.clear()
            self.ax.set_title("Minimum Spanning Tree")

            node_positions = {}
            for node in self.graph_data.arrayOfNodes:
                x, y = random.uniform(0, 10), random.uniform(0,
                                                             10)  # generating random positions for nodes as we did in the generate_graph function
                node_positions[node.data] = (x, y)
                self.ax.plot(x, y, 'o', label=f"Node {node.data}")
            labels = []
            for edge in mst:  # iterating through our mst to plot the edges and their weights
                start_node, end_node, weight = edge
                x1, y1 = node_positions[start_node]
                x2, y2 = node_positions[end_node]
                self.ax.plot([x1, x2], [y1, y2], 'g-',
                             label=f"Edge {start_node}-{end_node} (Weight: {weight})")  # MST edge
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                self.ax.text(mid_x, mid_y, str(weight), fontsize=8, color='blue')
                labels.append(f"Edge {start_node}-{end_node} (Weight: {weight})")
            legMST = self.ax.legend(loc="upper right", bbox_to_anchor=(1.02, 0, 0.1, 1), labels=labels)

            def scroll_leg(evt):
                d = {"down": 100, "up": -100}
                if legMST.contains(evt):
                    bbox = legMST.get_bbox_to_anchor()
                    bbox = Bbox.from_bounds(bbox.x0, bbox.y0 + d[evt.button], bbox.width, bbox.height)
                    tr = legMST.axes.transAxes.inverted()
                    legMST.set_bbox_to_anchor(bbox.transformed(tr))
                    self.figure.canvas.draw_idle()

            kruskal_time = endTime - startTime
            self.kruskal_time_label.setText(f"Kruskal's Algorithmn Time: {kruskal_time: .6f} seconds")
            self.figure.canvas.mpl_connect("scroll_event", scroll_leg)
            self.canvas.draw()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to calculate MST: {e}")

    def calculate_mstP(self):
        if not self.graph_data:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please first generate a graph.")
            return

        try:
            startTime = time.time()
            mst = prim(self.graph_data)  # calculating our mst using prim's algorithm
            endTime = time.time()
            #print("MST:", mst)  # code debug statement for our mst

            self.ax.clear()
            self.ax.set_title("Minimum Spanning Tree")

            node_positions = {}
            for node in self.graph_data.arrayOfNodes:
                x, y = random.uniform(0, 10), random.uniform(0,
                                                             10)  # generating random positions for nodes as we did in the generate_graph function
                node_positions[node.data] = (x, y)
                self.ax.plot(x, y, 'o', label=f"Node {node.data}")
            labels = []
            for edge in mst:  # iterating through our mst to plot the edges and their weights
                start_node, end_node, weight = edge
                x1, y1 = node_positions[start_node]
                x2, y2 = node_positions[end_node]
                self.ax.plot([x1, x2], [y1, y2], 'g-',
                             label=f"Edge {start_node}-{end_node} (Weight: {weight})")  # MST edge
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                self.ax.text(mid_x, mid_y, str(weight), fontsize=8, color='blue')
                labels.append(f"Edge {start_node}-{end_node} (Weight: {weight})")

            legMST = self.ax.legend(loc="upper right", bbox_to_anchor=(1.02, 0, 0.1, 1), labels=labels)

            def scroll_leg(evt):
                d = {"down": 100, "up": -100}
                if legMST.contains(evt):
                    bbox = legMST.get_bbox_to_anchor()
                    bbox = Bbox.from_bounds(bbox.x0, bbox.y0 + d[evt.button], bbox.width, bbox.height)
                    tr = legMST.axes.transAxes.inverted()
                    legMST.set_bbox_to_anchor(bbox.transformed(tr))
                    self.figure.canvas.draw_idle()
            prim_time = endTime - startTime
            self.prim_time_label.setText(f"Prim's Algorithmn Time: {prim_time: .6f} seconds")
            self.figure.canvas.mpl_connect("scroll_event", scroll_leg)
            self.canvas.draw()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to calculate MST: {e}")

    def algorithm_times(self, prim_time, kruskal_time):

        self.prim_time_label.setText(f"Prim's Algorithmn Time: {prim_time: .6f} seconds")
        self.kruskal_time_label.setText(f"Kruskal's Algorithmn Time: {kruskal_time: .6f} seconds")
