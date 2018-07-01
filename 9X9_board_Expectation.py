import CandyCrashSimulation3X3_2 as f
import random
import copy
import numpy as np

width = height = 3
s = 2 ** (width * height)
num_candy = 2
N = 100000
print("size: {} * {}".format(width,height))

w_score = np.zeros(s*N).reshape(s,N)
for i in range(s):
    board = f.buildboard(i, height, width)
    for c in range(N):
        newboard,tmp,score = f.eliminate_to_static(board,height,width)
        w_score[i][c] = score
mean = np.mean(w_score,axis=1)
std = np.std(w_score,axis=1)
with open('experiment_mean_std_width3_height3_candies2.txt','w') as fout:
    for i in range(s):
        fout.write("{} {} {}\n".format(i,mean[i],std[i]))
print("Done")

