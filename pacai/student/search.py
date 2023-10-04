"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""
from pacai.core.directions import Directions
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    
 
    """
    w = Directions.WEST
    dirs = {'North': Directions.NORTH, 
            'East': Directions.EAST, 
            'South': Directions.SOUTH,
            'West': Directions.WEST} 
    # *** Your Code Here ***
    path = problem.successorStates(problem.startingState())
    #while goal not found and stack not empty

    visited = [problem.startingState()]
    print(visited)
    
    while len(path) > 0:
        node = path.pop()
        visited.append(node[0])
       
        if problem.isGoal(node[0]):
            print("found")
            break
        for successor in problem.successorStates(node[0]):
            if not (successor[0] in visited):
                path.append(successor)
     
    return [dirs[tup[1]] for tup in path]

    #print([successor for successor in problem.successorStates(problem.startingState())])
    #print("Start:", problem.startingState())
    #print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    #print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
       
    #raise NotImplementedError()
    return [] 
def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    raise NotImplementedError()

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    raise NotImplementedError()

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    raise NotImplementedError()
