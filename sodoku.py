# Sodoku CS 4613
# Cynthia Cheng (cc5469) and Matthew Swartz (mcs871)  

# initial empty game board
board = []
# load in game board from input file and place into board array variable
def loadInputFile(filename):
    # open input file 
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
        for i in range(len(lines)):
            board.append([int(x) for x in lines[i].split()])

# LOAD THE INPUT FILE HERE
loadInputFile("Input1.txt")

# import proper libraries
import numpy as np
from functools import reduce

# convert board array to numpy array
sodukuBoard = np.asarray(board)
# this will be our tuples of 3 numbers for a row of a subgrid
slices = [slice(0,3), slice(3,6), slice(6,9)]
s1,s2,s3 = slices
allgrids=[(si,sj) for si in [s1,s2,s3] for sj in [s1,s2,s3]]

# finds the 3x3 grid slice the var coordinates belong in 
def varToGrid(var):
    row,col = var
    grid = ( slices[int(row/3)], slices[int(col/3)] )
    return grid

# value range of 1-9 stored in array
FULLDOMAIN = np.array(range(1,10))


# CONSTRAINTS
# check that the rows of the solution has no repeats, i.e. one 1, one 2, ... , one 9 per row
def unique_rows(sodukuBoard):
    for row in sodukuBoard:
        # if the row does not equal the array 1-9 then there is a repeat in the row, return false
        if not np.array_equal(np.unique(row), np.array(range(1,10))):
            return False
    return True
# check that the colums of the solution have no repeated 1-9 values
def unique_columns(sodukuBoard):
    #transpose soduku to get columns
    for col in sodukuBoard.T:
        # same as above, compare column to array [1, 2, 3, ... , 9] i.e. no duplicates
        if not np.array_equal(np.unique(col),np.array(range(1,10))) :
            return False
    return True
# check that each grid, the 9 3x3 squares, of the board have no repeated values
def unique_grids(sodukuBoard):
    for grid in allgrids:
        # check a 3x3 grid is equivalent to [1, 2, 3, ... , 9] i.e. no duplicates in the subgrid
        if not np.array_equal(np.unique(sodukuBoard[grid]),np.array(range(1,10))) :
            return False
    return True
# check the board for any 0's
def isComplete(sodukuBoard):
    if 0 in sodukuBoard:
        return False
    else:
        return True
# checks all our constraints to see if our board is a valid complete solution
def checkCorrect(sodukuBoard):
    if unique_columns(sodukuBoard):
        if unique_rows(sodukuBoard):
            if unique_grids(sodukuBoard):
                return True
    return False


# BACKTRACKING FUNCTIONS
# returns an array of the available values between 1-9 avaible for this square to keep it within the constraints above
def getDomainValues(var, sodukuBoard):
    row,col = var
    # this creates an array of numbers between 1-9 which already exist in this row, column, or subgrid 
    used_d = reduce(np.union1d, (sodukuBoard[row,:], sodukuBoard[:,col], sodukuBoard[varToGrid(var)]))
    # values left to pick from for this square to make sure it still satisfies thee constraint
    avail_d = np.setdiff1d(FULLDOMAIN, used_d)
    return avail_d

# Minimum Remaining Value Heuristic
def minimumRemainingVal(vars, sodukuBoard):
    # gets our ORDER-DOMAIN-VALUES for the remaining 0's left on our board
    avail_domains = [getDomainValues(var,sodukuBoard) for var in vars]
    # the number of values a remaning zero can be, i.e. the size of one of the domains in avail_domain
    avail_sizes = [len(avail_d) for avail_d in avail_domains]
    # the index of the domain with the smallest size
    index = np.argmin(avail_sizes)
    # return the tuple of the coordinates of the 0 being replaced, and its possible domains
    return vars[index], avail_domains[index]

# our actual backtracking algorithm
def backtrackingSearch(sodukuBoard):
    # solution is complete return the board
    if isComplete(sodukuBoard):
        return sodukuBoard
    # our tuples of the coordinates of the 0's left in the board
    vars = [tuple(e) for e in np.transpose(np.where(sodukuBoard==0))]
    # find our zero to replace based on the MRV heuristic
    var, avail_d = minimumRemainingVal(vars, sodukuBoard)
    # recursively solve and backtrack an assignment when stuck
    for value in avail_d:
        # set 0 = to new value
        sodukuBoard[var] = value
        # recusive call
        result = backtrackingSearch(sodukuBoard)
        # checks if a result of the value placement works
        if np.any(result):
            return result
        # reset board to zero as placement did not work with that number
        else:
            sodukuBoard[var] = 0
    # fails to find value
    return False


# Solve the board
backtrackingSearch(sodukuBoard)
checkCorrect(sodukuBoard)

# Write solution to output file
with open('output.txt','w') as f:
    output_str = ""
    # loop through solution array 
    for i in range(9):
        for j in range(9):
            # add number with a space
            output_str += (str(sodukuBoard[i][j]) + " ")
        # new line for each row
        output_str += "\n"
    
    f.write(output_str)

















    
