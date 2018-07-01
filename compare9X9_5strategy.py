import CandyCrashSimulationNXN_4 as S
import random
import copy
import numpy as np
import csv

def horizontal_or_vertical(board,r1,c1,d,height,width): # 0 mean horizontal; 1 mean vertical
    x = [ 0, 0, 0,-1, 1] # 1:up 2:down 3:left 4:right
    y = [ 0,-1, 1, 0, 0]
    r = r1 + y[d]
    c = c1 + x[d]
    if c+1 < width and c-1 >= 0:
        if (board[r1][c1] == board[r][c + 1] and board[r1][c1] == board[r][c - 1] and 
            not(r1 == r and c1 == c+1) and not(r1 == r and c1 == c-1)):
            return 0
    if c+2 < width:
        if (board[r1][c1] == board[r][c + 1] and board[r1][c1] == board[r][c + 2] and 
            not(r1 == r and c1 == c+1) and not(r1 == r and c1 == c+2)):
            return 0
    if c-2 >= 0:
        if(board[r1][c1] == board[r][c - 1] and board[r1][c1] == board[r][c - 2] and 
            not(r1 == r and c1 == c-1) and not(r1 == r and c1 == c-2)):
            return 0
    return 1 
def Ncompare(num_move):
    x = [ 0, 0, 0,-1, 1] # 1:up 2:down 3:left 4:right
    y = [ 0,-1, 1, 0, 0]
    width = height = 9
    num_candy = 4
    eachscore = np.zeros(9) 
    eachscore[0] = num_move
    N = 1000
    for i in range(N):
        o_board = S.initialize(height,width)
        #print("-----------------------------------------------------")
        board = copy.deepcopy(o_board)
        for j in range(num_move): # random move
            move = S.detect(board,height,width)
            if len(move) == 0:
                board = S.initialize(height,width)
                move = S.detect(board,height,width)
            ran = random.choice(move)
            board = S.swap(board,ran//100,(ran%100)//10,ran%10)
            board,tmp,score = S.eliminate_to_static(board,height,width)
            eachscore[1] += score
        #print("-----------------------------------------------------")
        board = copy.deepcopy(o_board)
        for j in range(num_move): # Vertical Elimination first
            move = S.detect(board,height,width)
            if len(move) == 0:
                board = S.initialize(height,width)
                move = S.detect(board,height,width)
            vmove = [] 
            for i in move:                 # possible move
                if horizontal_or_vertical(board,i//100,(i%100)//10,i%10,height,width):
                    vmove.append(i)
            if len(vmove) == 0:
                ran = random.choice(move)
            else:
                ran = random.choice(vmove)
            board = S.swap(board,ran//100,(ran%100)//10,ran%10)
            board,tmp,score = S.eliminate_to_static(board,height,width)
            eachscore[2] += score
        #print("-----------------------------------------------------")
        board = copy.deepcopy(o_board)
        for j in range(num_move): # Horizontal Elimination first
            move = S.detect(board,height,width)
            if len(move) == 0:
                board = S.initialize(height,width)
                move = S.detect(board,height,width)
            hmove = [] 
            for i in move:                 # possible move
                if not horizontal_or_vertical(board,i//100,(i%100)//10,i%10,height,width):
                    hmove.append(i)
            if len(hmove) == 0:
                ran = random.choice(move)
            else:
                ran = random.choice(hmove)
            board = S.swap(board,ran//100,(ran%100)//10,ran%10)
            board,tmp,score = S.eliminate_to_static(board,height,width)
            eachscore[3] += score
        #print("-----------------------------------------------------")
        board = copy.deepcopy(o_board)
        for j in range(num_move): # Vertical Elimination & Deeper first
            move = S.detect(board,height,width)
            
            if len(move) == 0:
                board = S.initialize(height,width)
                move = S.detect(board,height,width)
            vmove = [] 
            for i in move:                 # possible move
                if horizontal_or_vertical(board,i//100,(i%100)//10,i%10,height,width):
                    vmove.append(i)
            if len(vmove) == 0:
                ran = move[-1]
            else:
                vmove.sort()
                ran = vmove[-1]
            board = S.swap(board,ran//100,(ran%100)//10,ran%10)
            board,tmp,score = S.eliminate_to_static(board,height,width)
            eachscore[4] += score
        #print("-----------------------------------------------------")
        board = copy.deepcopy(o_board)
        for j in range(num_move): # Horizontal Elimination & Deeper first
            move = S.detect(board,height,width)
            if len(move) == 0:
                board = S.initialize(height,width)
                move = S.detect(board,height,width)
            hmove = [] 
            for i in move:                 # possible move
                if not horizontal_or_vertical(board,i//100,(i%100)//10,i%10,height,width):
                    hmove.append(i)
            if len(hmove) == 0:
                ran = move[-1]
            else:
                hmove.sort()
                ran = hmove[-1]
                
            #print(ran)
            board = S.swap(board,ran//100,(ran%100)//10,ran%10)
            board,tmp,score = S.eliminate_to_static(board,height,width)
            eachscore[5] += score
        #print("-----------------------------------------------------")
        board = copy.deepcopy(o_board)
        for j in range(num_move): # Horizontal Elimination & Deeper Center first
            move = S.detect(board,height,width)
            if len(move) == 0:
                board = S.initialize(height,width)
                move = S.detect(board,height,width)
            hmove = [] 
            for i in move:                 # possible move
                if not horizontal_or_vertical(board,i//100,(i%100)//10,i%10,height,width):
                    hmove.append(i)
            if len(hmove) == 0:
                move = sorted(move, key = lambda v: (v//100+y[v%10],abs((v%100)//10+x[v%10])-5))
                ran = move[-1]
            else:
                hmove = sorted(hmove, key = lambda v: (v//100+y[v%10],abs((v%100)//10+x[v%10])-5))
                ran = hmove[-1]
                
            #print(ran)
            board = S.swap(board,ran//100,(ran%100)//10,ran%10)
            board,tmp,score = S.eliminate_to_static(board,height,width)
            eachscore[6] += score
        #print("-----------------------------------------------------")
    eachscore[1:] /= N
    return eachscore

sresult = []
for i in range(1,50,1):
    tmp = Ncompare(i)
    sresult.append(tmp)
    print(tmp)

with open('compare9X9_5strategy.csv','w') as fout:
    writer = csv.writer(fout)
    writer.writerows(sresult)

