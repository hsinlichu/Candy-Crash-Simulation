import numpy
import sympy
from fractions import Fraction

def derive(h, height, width):
  rows = []
  for i in range(height):
    row = []
    for j in range(width):
      row.append(1 if h & (1 << (i * width + j)) else 0)
    rows.append(row)
  columns = []
  for j in range(width):
    column = []
    for i in range(height):
      column.append(1 if h & (1 << (i * width + j)) else 0)
    columns.append(column)
  # row elimination
  row_eliminate = []
  for i in range(height):
    if rows[i][1:] == rows[i][:-1]: # mean whole column are the same element
      row_eliminate.append(i)
  # column elimination
  column_eliminate = []
  for j in range(width):
    if columns[j][1:] == columns[j][:-1]:
      column_eliminate.append(j)
  # process
  for i in row_eliminate:
    rows.pop(i)
    rows = [[0] * height] + rows[:] # remove the eliminate row and replace with 0
  for j in column_eliminate:
    for i in range(height):
      rows[i][j] = 0
  new_h = 0
  for i in range(height):
    for j in range(width): # calculate new board number
      new_h += (rows[i][j] << (i * width + j))
  row_eliminate = list(range(len(row_eliminate))) # if we remove lower line, upper line would go down
  diff = set()                                    # so we only need to record the upper len(row_eliminate) are empty 
  for i in row_eliminate:                         # generate all the possible board after remove candy
    for j in range(width):
      diff.add(1 << (i * width + j))
  for i in range(height):
    for j in column_eliminate:
      diff.add(1 << (i * width + j))
  diff = list(diff)
  result = []
  for c in range(1 << len(diff)):
    summation = 0
    for d in range(len(diff)):
      if (c & (1 << d)):
        summation += diff[d]
    result.append(new_h + summation)
  result.sort()
  return [result, len(diff)]

def numpy_method(width, height):
  s = 2 ** (width * height)
  A = numpy.zeros(shape=(s, s))
  b = numpy.zeros(shape=(s, 1))
  for h in range(s):
    l, b[h][0] = tuple(derive(h, height, width))
    A[h][h] = 1
    if len(l) > 1:
      for d in l:
        A[h][d] -= 1 / len(l)
  result = numpy.linalg.solve(A, b)
  result.shape = (1, s)
  x = []
  for h in range(s):
    x.append(Fraction(result[0][h]).limit_denominator())
  return x

def sympy_method(width, height): # significantly slow but very precise
  s = 2 ** (width * height)
  A = sympy.zeros(s, s)
  b = sympy.zeros(s, 1)
  for h in range(s):
    l, b[h] = tuple(derive(h, height, width))
    A[h, h] = sympy.Rational(1)
    if len(l) > 1:
      for d in l:
        A[h, d] -= sympy.Rational(1, len(l))
  result = A.LUsolve(b)
  result = list(result)
  return list(result)

# parameters
width = 3
height = 3
s = 2 ** (width * height)

result_list = numpy_method(width, height)
for h in range(s):
  print(h, result_list[h])
