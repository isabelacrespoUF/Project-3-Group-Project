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

