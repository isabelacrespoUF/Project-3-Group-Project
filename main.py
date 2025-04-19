from PyQt5 import QtWidgets
import sys
from gui import MSTGUI
from algorithms import prim, kruskal
from dataset import data
import time
maxConnect = 4
noNodes = 5
datastuff = data(noNodes, maxConnect)
datastuff.generate()
startTime = time.time()
primArr = prim(datastuff)
endTime = time.time()
primTime = endTime - startTime # display time taken for prim's algorithm in GUI

startTime = time.time()
kruskalArr = kruskal(datastuff)
endTime = time.time()
kruskalTime = endTime - startTime # display time taken for kruskal's algorithm in GUI


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MSTGUI()
    window.show()
    sys.exit(app.exec_())

