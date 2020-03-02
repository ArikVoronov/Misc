# Sudoku Solver:
import numpy as np

class Cell():
    def __init__(self):
        self.blocked

class KlotskyPuzzle():
    pass


def Possible(r,c,n,grid):
    if n in grid[r,:]:
        return False
    if n in grid[:,c]:
        return False
    # check 3x3 square
    r0 = r//3; c0 = c//3
    if n in grid[3*r0:3*r0+3,3*c0:3*c0+3]:
        return False
    return True

def CreateSudoku(clearCount):
    grid = np.matrix(np.zeros([9,9]))
    for i in range(9):
        n = 0
        while not Possible(0,i,n,grid):
            n = np.random.randint(1,10)
        grid[0,i] = n
    FillSudoku(grid)
    cleared = []
    for _ in range(clearCount):
        cell = (np.random.randint(9),np.random.randint(9))
        grid[cell[0],cell[1]] = 0
        while cell in cleared:
            cell = (np.random.randint(1,10),np.random.randint(1,10))
            grid[cell[0],cell[1]] = 0
    return grid
    
    

def FillSudoku(grid):
    filled = False
    for r in range(9):
        for c in range(9):
            if grid[r,c]==0:
                for n in range(1,10):
                    if Possible(r,c,n,grid):
                        grid[r,c] = n
                        filled = FillSudoku(grid)
                        
                        if filled:
                            break
                        else:
                            grid[r,c]=0
                return filled
    return True


if __name__ == "__main__":
    grid = CreateSudoku(80)
    print('New Sudoku:')
    print(grid)
    FillSudoku(grid)
    print('Solved:')
    print(grid)
                    
            
    
    
    
