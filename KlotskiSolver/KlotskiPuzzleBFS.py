'''
Klotski puzzle solver,
KP states are viewed as nodes in an undirected graph, 
a breadth first search (BFS) algorithm is used to find the shortest path
from the intial state to the victory condition state

Author: Arik Voronov
Date: 01.03.20
'''

from KlotskiPuzzle import *        

def BreadthFirstSearch(KP):
    '''
    Stores KP objects as graph nodes,
    an incomplete graph is created as the function runs.
    Finds all paths to solution using a BFS.

    Parameters
    ----------
    KP : KlotskiPuzzle object
        initial state of the puzzle grid.

    Returns
    -------
    solutionPaths : list 
        list of lists containing KP objects.
    '''
    start = KP
    queue = []
    queue.append(start)
    visited=set(GridHashKey(start.grid))
    solutionPaths = []
    while (len(queue)>0):
        current = queue.pop(0)
        neighbors = GetNeighbors(current)
        for nextNode in neighbors:
            hashed = GridHashKey(nextNode.grid)
            if hashed in visited:
                continue
            # if not in visited, add the hash key (and mirror) to visited
            nextNode.previousBoard = current # Remember which state reached this node
            nextNode.distance = current.distance+1
            visited.add(hashed)
            visited.add(GridHashKey(MirrorGrid(nextNode.grid))) #Mirror the grid hashkey - that's not a unique new state
            if nextNode.GameWon(): #There's no more branching after the game is won, so don't add it to the queue
                solutionPaths.append(GetSolutionPath(nextNode))
            else:
                queue.append(nextNode)

    return solutionPaths

def GetNeighbors(KP):
    '''
    Get all neighboring states (nodes) to the current KP

    Parameters
    ----------
    puzzle : KlotskiPuzzle object
        current state.

    Returns
    -------
    neighbors : list
        list of neighboring KP objects.
    '''
    neighbors =[]
    valids = KP.GetAllValidActions()
    for block,action in valids:
        neighbors.append(KP.MoveBlock(block,action))
    return neighbors

def GetSolutionPath(KP):
    '''
    Get the path to the input KP, untill reaches the initial state (no parent)

    Parameters
    ----------
    board : KlotskiPuzzle object
        last state in the path.

    Returns
    -------
    path : list
        list of KP objects [intial state ->...-> input state] (intial first).
    '''
    path = []
    while KP != None:
        path.insert(0,KP)
        KP = KP.previousBoard
    return path

if __name__ =="__main__":
    KP = CreateNewKP(5,4)
    solutionPaths = BreadthFirstSearch(KP)
    pathLengths = [i for i in map(len,solutionPaths)]
    print('Found {} unique solution paths'.format(len(solutionPaths)))
    print('Shortest path has {} steps'.format(min(pathLengths)))
