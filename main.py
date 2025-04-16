#CAN CHANGE EVERYTHING IN MAIN

from dataset import data

maxConnect = 4
noNodes = 100000
datastuff = data(noNodes, maxConnect)
datastuff.generate()
count = 0
for i in range(noNodes):
    if len(datastuff.arrayOfNodes[i].getConnections()) == maxConnect:
        count += 1
print(count)