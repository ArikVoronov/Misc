'''
Klotski puzzle class and helper functions
 

Author: Arik Voronov
Date: 01.03.20
'''
class Block():
    '''
    A block object which populates the Klotski grid.
    '''
    def __init__(self,number,cells,target = False):
        self.number = number
        self.cells = cells
        self.target = target # This is the block which must get to the goal
        self.actionKeys = [(-1,0),(0,1),(1,0),(0,-1)]
    def Move(self,action):
        if action not in [0,1,2,3]:
            print('Invalid action key')
            return self.cells
        shift = self.actionKeys[action]
        newCells = []
        for c in self.cells:
            newCells.append((c[0]+shift[0],c[1]+shift[1]))
        return newCells

class KlotskiPuzzle():
    '''
    Stores a Klotski puzzle grid and enables valid block movements.
    Defines the winning condition.
    Valid actions for movement : [0:up, 1:right, 2:down, 3:left]
    '''
    def __init__(self,rows,cols,blockList,grid):
        self.rows = rows
        self.cols = cols
        self.blockList = blockList
        self.previousBoard = None
        self.grid=grid
        self.distance = 0
        self.actionKeys = [(-1,0),(0,1),(1,0),(0,-1)]
    def MoveBlock(self,blockNumber,action):
        '''
        Creates a new block, moved according to the input action, 
        returns a new KP with a moved block 
        
        ** DOESN'T CHECK IF THE MOVE IS LEGAL **

        Parameters
        ----------
        blockNumber : int
            number of the block to move
        action : int
            action key 

        Returns
        -------
        KP object
            A new grid with a moved block.
        '''
        if action not in [0,1,2,3]:
            print('Invalid action key')
            return self
        # This assumes the action is valid for the given block
        block = self.blockList[blockNumber-1]
        newGrid = []
        for r in self.grid:
            newGrid.append(list(r))
        for c in block.cells:
            newGrid[c[0]][c[1]]=0
        newBlock = Block(block.number,block.Move(action),block.target)
        for c in newBlock.cells:
            newGrid[c[0]][c[1]]=newBlock.number
        blockList = list(self.blockList)
        blockList[blockNumber-1] = newBlock
        return KlotskiPuzzle(self.rows,self.cols,blockList,newGrid)  
    def GetAllValidActions(self):
        ''' Get all legal [block,action] pairs in the current state'''
        validList = []
        for action in [0,1,2,3]:
            for block in self.blockList:
                if self.LegalMove(block,action):
                    validList.append([block.number,action])
        return validList 
    def LegalMove(self,block,action):
        ''' Check if block can be moved using the input action '''
        shift = self.actionKeys[action]
        for cell in block.cells:
            r = cell[0]; c = cell[1]
            nr = r + shift[0]
            nc = c + shift[1]
            if nc <0 or nc>= self.cols:# out of bounds
                return False
            if nr <0 or nr>= self.rows:# out of bounds
                return False
            gvalue = self.grid[nr][nc]
            if gvalue not in [0,block.number]:
                return False
        return True
    def GameWon(self):
        if self.grid[4][1] ==10 and self.grid[4][2]==10:
            return True
        return False
    def RenderInConsole(self):
        print('\n')
        for r in range(self.rows):
            print('|',end='')
            for c in range(self.cols):
                n = self.grid[r][c]
                if type(n)==int:
                    if n<10:
                        print(' '+str(n),end=' |')
                    else:
                        print(n,end=' |')
                else:
                    print(' ' + str(n),end=' |')
            print('\n')


# Helper functions
def CreateNewKP(rows,cols):
    grid = [[1,10,10,4],
            [1,10,10,4],
            [2, 7, 7,5],
            [2, 8, 9,5],
            [3, 0, 0,6],
            ]
    blockList = []
    for v in range(1,11):
        blockCells = [(r,c) for c in range(cols) for r in range(rows) if grid[r][c]==v]
        blockList.append(Block(v,blockCells))
    blockList[-1].target = True             
    return KlotskiPuzzle(rows,cols,blockList,grid)

def GridHashKey(grid):
    '''
    Creates a unique hash string representing the grid, this is used to quickly
    search for visited states.
    Blocks of identical dimensions are given the same hash key.

    Parameters
    ----------
    grid : list
        KP grid.

    Returns
    -------
    hashed : string
        unique hashed string.

    '''
    value_map = {0: ' ', 1: 'v', 2: 'v', 3: 's', 4: 'v', 5: 'v', 6: 's', 7: 'h', 8: 's',9:'s',10:'t',-2:'e', -1: 'w'}
    chars = [value_map[s] for r in grid for s in r ]
    hashed = ''.join(chars)
    return hashed

def Render(grid):
    rows = len(grid)
    cols = len(grid[0])
    print('\n')
    for r in range(rows):
        print('|',end='')
        for c in range(cols):
            n = grid[r][c]
            if type(n)==int:
                if n<10:
                    print(' '+str(n),end=' |')
                else:
                    print(n,end=' |')
            else:
                print(' ' + str(n),end=' |')
        print('\n')

def MirrorGrid (grid):
    '''
    Create a mirror grid , used for adding mirror hashes to the visited states
    since the game is symmetric about the vertical axis, mirrored grids aren't
    new states.
    
    Parameters
    ----------
    grid : list
        KP grid.

    Returns
    -------
    mirrorGrid : list
        Mirrored KP grid.
    '''
    mirrorGrid  =[]
    for r in range(len(grid)):
        newRow = list(grid[r])
        newRow.reverse()
        mirrorGrid.append(newRow)
    return mirrorGrid
def ReverseAction(action):
    ''' Reverse the input action '''
    return ( action+2)%4

def MoveByPath(KP,path):
    '''
    Moves along a path and renders the board at every move

    Parameters
    ----------
    KP : KP object
        initial state.
    path : list
        list of [block,action] couples.
    '''
    for p in path:
        block = p[0]
        action = p[1]
        KP = KP.MoveBlock(block,action)
        KP.RenderInConsole()

def MoveByKP(path):
    '''
    Moves along a path and renders the board at every move

    Parameters
    ----------
    KP : KP object
        initial state.
    path : list
        list of [KP] objects with different grid stats.
    '''
    for KP in path:
        KP.RenderInConsole()
if __name__ == "__main__":
    pass
