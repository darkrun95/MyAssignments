"""
7 Queens - mpi4py using 7 processes - 1 master + 7 slaves
"""
from mpi4py import MPI 
import json
import numpy as np

size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()

positions = []
column = None
def check_queen(board, row, col):
    if board[row][col] > 0:
        return False

    for i in range(4):
        if board[row][i] > 0:
            return False

    for i in range(4):
        if board[i][col] > 0:
            return False

    for i in range(4):
        if row - i >= 0 and col - i >= 0:
            if board[row-i][col-i] > 0:
                return False
        if row + i < 4 and col + i < 4:
            if board[row+i][col+i] > 0:
                return False
        if row - i >= 0 and col + i < 4:
            if board[row-i][col+i] > 0:
                return False
        if row + i < 4 and col - i >= 0:
            if board[row+i][col-i] > 0:
                return False
    return True

def generate_positions():
    initial_queen_pos = None
    queens = None
    column = None

    queens = MPI.COMM_WORLD.bcast(queens, root=0)
    column = MPI.COMM_WORLD.bcast(column, root=0)

    if check_queen(queens, rank-1, column):
        positions.append(MPI.COMM_WORLD.gather([1, rank-1], root=0))
    else:
        positions.append(MPI.COMM_WORLD.gather([0, rank-1], root=0))
    return 

def place_queens(column):
    MPI.COMM_WORLD.bcast(queens, root=0)
    MPI.COMM_WORLD.bcast(column, root=0)

    positions = MPI.COMM_WORLD.gather(None, root=0)
    positions.pop(0)

    if column == 0:
        for x in range(queens.__len__()):
            if queens[x][column] <> -1 and x not in rows_occupied:
                queens[x][column] = 1
                rows_occupied.append(x)
                queens[queens == -1] = 0
                return True

        print "No solution available"
        MPI.COMM_WORLD.Abort()
        exit()
    else:
        for items in positions:
            if items[0] == 1 and queens[items[1]][column] <> -1:
                queens[items[1]][column] = 1
                return True
        return False

if rank == 0:
    column = 1
    data = None
    queens = np.zeros(shape=(4,4))
    initial_queen_pos = 0
    with open("data.json") as fh:
        data = json.load(fh)
    initial_queen_pos = data['queen']
    queens[initial_queen_pos][0] = 1
    rows_occupied = [initial_queen_pos]

while True:
    if rank == 0:
        if column == 4:
            print "Solution found"
            queens[queens == -1] = 0
            MPI.COMM_WORLD.Abort()

        if place_queens(column):
            column += 1
        else:
            column -= 1
            for x in queens:
                if x[column] == 1:
                    x[column] = -1                    

        for x in queens:
            print x
        print

    else:
        generate_positions() 
        
"""
data.json - indicating initial queen position

{
    "queen":3
}

"""