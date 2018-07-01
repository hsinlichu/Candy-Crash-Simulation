import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import csv

data = []
with open('ExpectationCompare.csv', 'r') as fin:
    reader = csv.reader(fin)
    data = list(reader)
board = []
samplemean = []
std = []
truemean = []

for row in data:
    board.append(int(row[0]))
    samplemean.append(float(row[1]))
    truemean.append(float(row[2]))
    if float(row[5]) == 0:
        std.append(0)
    else:
        std.append(float(row[5]))
nstd = (np.array(std)/np.sqrt(1000))
nstd = [1 if i == 0 else i for i in nstd]
samplemean = np.array(samplemean)
truemean = (np.array(truemean) - np.array(samplemean))/nstd
interval = (1.96*np.array(std)/np.sqrt(1000))/nstd
out = np.array([1 if i < 1.96 else 0 for i in truemean])
print("In the interval:",out.sum()/len(out))

samplemean = list(np.zeros(len(samplemean)))
plt.errorbar(x=board,y=list(samplemean),yerr=list(interval),fmt='.',markersize='0.8',capsize=2, elinewidth=0.5)
plt.plot(board,list(truemean),color="red", marker='o',linestyle='None', markersize=2)
plt.title('Normalized 95% Confidence Inteveral')
plt.show()
plt.savefig('95%_Confidence_Inteveral_Normalized.png')

