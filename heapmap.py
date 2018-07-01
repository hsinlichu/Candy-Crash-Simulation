import random
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import CandyCrashSimulationNXN_4 as f

width = height = 9
num_candy = 4
N = 100
print("size: {} * {}".format(width,height))

heatmap = np.zeros(width * height).reshape(height,width ) 
for i in range(N):
    board = f.initialize(height,width)
    board[8][3] = 1
    board[8][3 + 1] = 1
    board[8][3 + 2] = 1
    newboard,mark,score = f.eliminate_to_static(board,height,width)
    heatmap += mark
heatmap /= N
print(heatmap)

trace = go.Heatmap(z=[[1,2,3],[4,5,6],[7,8,9]])
# ,x=['0','1','2','3','4','5','6','7','8'],y=['0','1','2','3','4','5','6','7','8']
data = [trace]
plotly.offline.iplot(data,filename='EliminateCandyLocation')
