# Sodoku CS 4613
# Cynthia Cheng (cc5469) and Matthew Swartz (mcs871)  

board = []
def loadInputFile(filename):
    # open input file 
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
        for i in range(len(lines)):
            board.append([int(x) for x in lines[i].split()])
    return board 

print(loadInputFile("Sample_Input.txt"))


# def printBoard(board):
#     for i in range(0, 9):
#         for j in range(0, 9):
#             print(board[i][j], end=" ")
#         print()

# def isPossible(board, row, col, val):
#     for j in range(0, 9):
#         if board[row][j] == val:
#             return False

#     for i in range(0, 9):
#         if board[i][col] == val:
#             return False

#     startRow = (row // 3) * 3
#     startCol = (col // 3) * 3
#     for i in range(0, 3):
#         for j in range(0, 3):
#             if board[startRow+i][startCol+j] == val:
#                 return False
#     return True

# def solve():
#     for i in range(0, 9):
#         for j in range(0, 9):
#             if board[i][j] == 0:
#                 for val in range(1, 10):
#                     if isPossible(board, i, j, val):
#                         board[i][j] = val
#                         solve()

#                         # Bad choice, make it blank and check again
#                         board[i][j] = 0
#                 return
#     # We found a solution, print it            
#     printBoard(board)
# print("\n\n")
# printBoard(board)
# print("\n\n")
# solve()

import sys
import numpy as np
from functools import reduce


soduku = np.asarray(board)

slices = [slice(0,3), slice(3,6), slice(6,9)]
s1,s2,s3 = slices
allgrids=[(si,sj) for si in [s1,s2,s3] for sj in [s1,s2,s3]] # Makes 2d slices for grids

def var2grid(var):
    "Returns the grid slice (3x3) to which the variable's coordinates belong "
    row,col = var
    grid = ( slices[int(row/3)], slices[int(col/3)] )
    return grid

FULLDOMAIN = np.array(range(1,10)) #All possible values (1-9)


# Constraints
def unique_rows(soduku):
    for row in soduku:
        if not np.array_equal(np.unique(row),np.array(range(1,10))) :
            return False
    return True
def unique_columns(soduku):
    for row in soduku.T: #transpose soduku to get columns
        if not np.array_equal(np.unique(row),np.array(range(1,10))) :
            return False
    return True

def unique_grids(soduku):
    for grid in allgrids: 
        if not np.array_equal(np.unique(soduku[grid]),np.array(range(1,10))) :
            return False
    return True

def  isComplete(soduku):
    if 0 in soduku:
        return False
    else:
        return True


def checkCorrect(soduku):
    if unique_columns(soduku):
        if unique_rows(soduku):
            if unique_grids(soduku):
                return True
    return False


# Search
def getDomain(var, soduku):
    "Gets the remaining legal values (available domain) for an unfilled box `var` in `soduku`"
    row,col = var
    #ravail = np.setdiff1d(FULLDOMAIN, soduku[row,:])
    #cavail = np.setdiff1d(FULLDOMAIN, soduku[:,col])
    #gavail = np.setdiff1d(FULLDOMAIN, soduku[var2grid(var)])
    #avail_d = reduce(np.intersect1d, (ravail,cavail,gavail))
    used_d = reduce(np.union1d, (soduku[row,:], soduku[:,col], soduku[var2grid(var)]))
    avail_d = np.setdiff1d(FULLDOMAIN, used_d)
    #print(var, avail_d)
    return avail_d

def selectMRVvar(vars, soduku):
    """
    Returns the unfilled box `var` with minimum remaining [legal] values (MRV) 
    and the corresponding values (available domain)
    """
    #Could this be improved?
    avail_domains = [getDomain(var,soduku) for var in vars]
    avail_sizes = [len(avail_d) for avail_d in avail_domains]
    index = np.argmin(avail_sizes)
    return vars[index], avail_domains[index]

def BT(soduku):
    "Backtracking search to solve soduku"
    # If soduku is complete return it.
    if isComplete(soduku):
        return soduku
    # Select the MRV variable to fill
    vars = [tuple(e) for e in np.transpose(np.where(soduku==0))]
    var, avail_d = selectMRVvar(vars, soduku)
    # Fill in a value and solve further (recursively), 
    # backtracking an assignment when stuck
    for value in avail_d:
        soduku[var] = value
        result = BT(soduku)
        if np.any(result):
            return result
        else:
            soduku[var] = 0
    return False


# Solve
print("solved:\n", BT(soduku))
print("correct:", checkCorrect(soduku))


# Output
with open('output.txt','w') as f:
    output_str = np.array2string(soduku.ravel(), max_line_width=90, separator='').strip('[]') + ' Solved with BTS'
    f.write(output_str)