import os
import sys
import numpy as np
import os.path
import copy
from random import randint

def encode(board, height, width):
    answer = 0
    mask = 0
    for i in range(height):
        for j in range(width):
            mask = board[i][j] 
            answer |= mask << ((height - 1 - i) * width + (width - 1 - j)) 
    return answer
        
def printbit(board, height, width):
    size = height * width
    for i in range(size):
        print(board >> (size - 1 - i) & 1,end = '')
    print("\n")
    return

def buildboard(board, height, width):
    element_mask = 1
    ret = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(board >> ((height - 1 - i) * width + (width - 1 - j)) & element_mask)
        ret.append(row)
    return ret

def detect(board, height, width):
  lx = [-2,-1,-1]
  ly = [ 0,-1, 1]
  lm = [ 4, 2, 1]  # 1:up 2:down 3:left 4:right
  rx = [ 2, 1, 1]
  ry = [ 0,-1, 1]
  rm = [ 3, 2, 1]  # 1:up 2:down 3:left 4:right
  move = []
  for i in range(height):                    # OO  |   O | O   |  OO 
    for j in range(width - 1):               #   O | OO  |  OO | O 
      if board[i][j] == board[i][j + 1]:
        for d in range(3): # left
          if i + ly[d] < 0 or i + ly[d] >= height or j + lx[d] < 0 or j + lx[d] >= width:
            continue
          if board[i + ly[d]][j + lx[d]] == board[i][j]:
            tmp = (i + ly[d]) * 100 + (j + lx[d]) * 10 + lm[d]
            if tmp not in move:
                move.append(tmp)
        for d in range(3): # Right
          if i + ry[d] < 0 or i + ry[d] >= height or j + 1 + rx[d] < 0 or j + 1 + rx[d] >= width:
            continue
          if board[i + ry[d]][j + 1 + rx[d]] == board[i][j + 1]:
            tmp = (i + ry[d]) * 100 + (j + 1 + rx[d]) * 10 + rm[d]
            if tmp not in move:
                move.append(tmp)

  ux = [ 0,-1, 1]
  uy = [-2,-1,-1]
  um = [ 2, 4, 3]  # 1:up 2:down 3:left 4:right
  dx = [ 0,-1, 1]
  dy = [ 2, 1, 1]
  dm = [ 1, 4, 3]  # 1:up 2:down 3:left 4:right
  
  for i in range(height - 1):            # O  |  O | O  |  O 
    for j in range(width):               # O  |  O |  O | O 
      if board[i][j] == board[i + 1][j]: #  O | O  |  O | O
        for d in range(3): # Up
          if i + uy[d] < 0 or i + uy[d] >= height or j + ux[d] < 0 or j + ux[d] >= width:
            continue
          if board[i + uy[d]][j + ux[d]] == board[i][j]:
            tmp = ((i + uy[d]) * 100 + (j + ux[d]) * 10 + um[d])
            if tmp not in move:
                move.append(tmp)
        for d in range(3): # Down
          if i + 1 + dy[d] < 0 or i + 1 + dy[d] >= height or j + dx[d] < 0 or j + dx[d] >= width:
            continue
          if board[i + 1 + dy[d]][j + dx[d]] == board[i][j]:
            tmp = (i + 1 + dy[d]) * 100 + (j + dx[d]) * 10 + dm[d]
            if tmp not in move:
                move.append(tmp)
              
  # horizontal
  hx = [ 1, 1]
  hy = [-1, 1]
  hm = [ 2, 1]  # 1:up 2:down 3:left 4:right
  for i in range(height):                    #   O  |     |
    for j in range(width - 2):               #  O O | O O |
      if board[i][j] == board[i][j + 2]:     #      |  O  |
        for d in range(2): 
          if i + hy[d] < 0 or i + hy[d] >= height or j + hx[d] < 0 or j + hx[d] >= width:
            continue
          if board[i + hy[d]][j + hx[d]] == board[i][j]:
            tmp = (i + hy[d]) * 100 + (j + hx[d]) * 10 + hm[d]
            if tmp not in move:
                move.append(tmp)
  # vertical
  vx = [ 1,-1]
  vy = [ 1, 1]
  vm = [ 3, 4]  # 1:up 2:down 3:left 4:right
  for i in range(height - 2):                # O  |  O |  
    for j in range(width):                   #  O | O  | 
      if board[i][j] == board[i + 2][j]:     # O  |  O | 
        #print("({},{})({},{})".format(i,j,i + 2,j))
        for d in range(2): 
          if i + vy[d] < 0 or i + vy[d] >= height or j + vx[d] < 0 or j + vx[d] >= width:
            continue
          if board[i + vy[d]][j + vx[d]] == board[i][j]:
            tmp = (i + vy[d]) * 100 + (j + vx[d]) * 10 + vm[d]
            if tmp not in move:
                move.append(tmp)
  return move # return a dictionary {location:direction}
def eliminate(board,height,width):  # clean board
    cnt = 0
    mark = [[0 for i in range(width)] for i in range(height)] # 1 mean removed
    # horizontal check
    for i in range(height):
        for j in range(width - 2):
            if board[i][j] == board[i][j + 1] and board[i][j + 1] == board[i][j + 2]:
                if mark[i][j] == 0:
                    mark[i][j] = 1
                    cnt += 1
                if mark[i][j + 1] == 0:
                    mark[i][j + 1] = 1
                    cnt += 1
                if mark[i][j + 2] == 0:
                    mark[i][j + 2] = 1
                    cnt += 1
                
    # vertical check
    for i in range(height - 2):
        for j in range(width):
            if board[i][j] == board[i + 1][j] and board[i + 1][j] == board[i + 2][j]:
                if mark[i][j] == 0:
                    mark[i][j] = 1
                    cnt += 1
                if mark[i + 1][j] == 0:
                    mark[i + 1][j] = 1
                    cnt += 1
                if mark[i + 2][j] == 0:
                    mark[i + 2][j] = 1
                    cnt += 1
    # remove
    board_t = np.array(board).transpose().tolist()
    mark_t = np.array(mark).transpose()
    for i in range(height):
        for j in range(width):
            if mark_t[i][j]:
                del board_t[i][j]
                board_t[i].insert(0,randint(0,1))
    board = np.array(board_t).transpose().tolist()
    return board,np.array(mark),cnt

def eliminate_to_static(board,height,width):
    totalscore = 0
    board,removedloc,score = eliminate(board,height,width)
    totalscore += score
    while score > 0:
        board,mark,score = eliminate(board,height,width)
        removedloc += mark
        totalscore += score
    return board,removedloc,totalscore

def initialize(height,width):
    board = [[randint(0,1) for i in range(width)] for i in range(height)]
    board,mark,tmp = eliminate_to_static(board,height,width)
    #print(board)
    return board

def swap(board,r1,c1,d):
    newboard = copy.deepcopy(board)
    x = [ 0, 0, 0,-1, 1] # 1:up 2:down 3:left 4:right
    y = [ 0,-1, 1, 0, 0]
    r2 = r1 +y[d]
    c2 = c1 +x[d]
    tmp = newboard[r1][c1]
    newboard[r1][c1] = newboard[r2][c2]
    newboard[r2][c2] = tmp
    return copy.deepcopy(newboard)

'''
### Preview ###
  0   1   2   3   4 \n
----+---+---+---+---+\n
| {} | {} | {} | {} | {} | 0\n
----+---+---+---+---+\n
| {} | {} | {} | {} | {} | 1\n
----+---+---+---+---+\n
| {} | {} | {} | {} | {} | 2\n
----+---+---+---+---+\n
| {} | {} | {} | {} | {} | 3\n
----+---+---+---+---+\n
| {} | {} | {} | {} | {} | 4\n
----+---+---+---+---+\n"
'''

def printboard(board):
    
    grid = "  0   1   2 \n----+---+---+\n| {} | {} | {} | 0\n----+---+---+\n| {} | {} | {} | 1\n----+---+---+\n| {} | {} | {} | 2\n----+---+---+\n"
    print(grid.format(board[0][0],board[0][1],board[0][2],
                      board[1][0],board[1][1],board[1][2],
                      board[2][0],board[2][1],board[2][2]))
    return

### main program ###
if __name__ == "__main__":
    #width = int(sys.argv[1])
    #height = int(sys.argv[1])
    width = height = 3
    s = 2 ** (width * height)
    print("size: {} * {}".format(width,height))
    total_score = 0
    board = initialize(height,width)
    printboard(board)
    while True:
        move = detect(board,height,width)
        move.sort()
        print(len(move))
        print("Possible move:")
        for i in move:                 # possible move
            print("({},{}) -> {}".format(i//100,(i%100)//10,i%10))
        print("Which candy you want to move and direction ? <row> <column> <direction>")
        print("Direction 1:up 2:down 3:left 4:right")
        r,c,d = input().split(' ')
        board = swap(board,int(r),int(c),int(d))
        print("After Swap")
        printboard(board)
        board,tmp,score = eliminate_to_static(board,height,width)
        print(tmp)
        total_score += score
        print("Static State")
        print("current score: {}".format(total_score))
        printboard(board)
