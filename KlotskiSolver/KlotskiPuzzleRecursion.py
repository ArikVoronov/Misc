'''
Klotski puzzle solver,
Using backtracking recursion, move through all valid states,
At each state of the puzzle, move every valid block/action
when the winning position is obtained, 
the recursion back tracks and stores the path to that point

Author: Arik Voronov
Date: 01.03.20
'''

from KlotskiPuzzle import *

def SolveKlotski(KP,visited,path):
    '''
    Backtracking recursive solution for KP
   
    Parameters
    ----------
    KP : Klotski Puzzle object
        current state of KP.
    visited : set
        grid states already visited during this recursion.
    path : list
        [block,action] couples, intial state ->...-> victory state
        initialized as an empty list)

    Returns
    -------
    bool
        True if reached the victory KP state.
    '''
    if KP.GameWon():
        return True
    valids = KP.GetAllValidActions() # [block,action pairs of all possible actions in state]
    neighbors = [] # List neighboring KP objects
    for block,action in valids:
        newKP = KP.MoveBlock(block,action)
        hashed = GridHashKey(newKP.grid)
        if hashed in visited: # If the new state has been visited before - reverse
            continue
        else:
            neighbors.append(newKP)
            visited.add(hashed)
            visited.add(GridHashKey(MirrorGrid(newKP.grid)))
    for newKP in neighbors:
        won = SolveKlotski(newKP,visited,path)
        if won: # Keep returning True and exit the recursion completely in the current state
            path.append([block,action])
            return True
    return False



if __name__ =="__main__":
    import sys
    sys.setrecursionlimit(5000) # Default value is 1000
    KP = CreateNewKP(5,4)
    KP.RenderInConsole()
    visited = set()
    path = []
    SolveKlotski(KP,visited,path)
    print('Found a solution path which has {} steps'.format(len(path)))


