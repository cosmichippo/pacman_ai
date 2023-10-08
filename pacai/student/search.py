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

    dirs = {'North': Directions.NORTH, 
            'East': Directions.EAST, 
            'South': Directions.SOUTH,
            'West': Directions.WEST} 
    # *** Your Code Here ***
    stack = [[pos, [direction]] for pos, direction, weight in problem.successorStates(problem.startingState())]
    #while goal not found and stack not empty
    visited = [problem.startingState()]

    while len(stack) > 0:
        
        n_pos, ls = stack.pop()

        visited.append(n_pos) 
        if problem.isGoal(n_pos):
            return [dirs[x] for x in ls] 
        for pos, direction, weight in problem.successorStates(n_pos):
            if not (pos in visited):
                sh_copy = ls.copy() 
                sh_copy.append(direction)
                stack.append([pos, sh_copy])
    return []



def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    dirs = {'North': Directions.NORTH, 
            'East': Directions.EAST, 
            'South': Directions.SOUTH,
            'West': Directions.WEST} 
    # *** Your Code Here ***
    stack = [[pos, [direction]] for pos, direction, weight in problem.successorStates(problem.startingState())]
    #while goal not found and stack not empty
    visited = [problem.startingState()]

    while len(stack) > 0:
        
        n_pos, ls = stack.pop(0)

        visited.append(n_pos) 
        if problem.isGoal(n_pos):
            return [dirs[x] for x in ls] 
        for pos, direction, weight in problem.successorStates(n_pos):
            if not (pos in visited):
                sh_copy = ls.copy() 
                sh_copy.append(direction)
                stack.append([pos, sh_copy])
    return []



def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """    # *** Your Code Here ***
    
    stack = [[pos, [direction], cost] for pos, direction, cost in problem.successorStates(problem.startingState())]
    #while goal not found and stack not empty
    visited = {problem.startingState(): 0}

    while len(stack) > 0:
        stack.sort(key = lambda x: x[2])
      
        n_pos, ls, n_cost = stack.pop(0)

        visited[n_pos] = problem.actionsCost(ls) 
        if problem.isGoal(n_pos):
            return ls 
        #sorted_successors = sorted(problem.successorStates(n_pos), key = lambda x: x[2] )

        for pos, direction, cost in problem.successorStates(n_pos):
            if not (pos in visited) or problem.actionsCost(ls + [direction]) < visited[pos]:
                sh_copy = ls.copy() 
                sh_copy.append(direction)
                stack.append([pos, sh_copy, problem.actionsCost(sh_copy)])

    return []


    # *** Your Code Here ***
    raise NotImplementedError()

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    raise NotImplementedError()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves `tinyMaze`.
    For any other maze, the sequence of moves will be incorrect,
    so only use this for `tinyMaze`.
    """
    #print(problem.getsuccessors(problem.startState()))
    s = Directions.SOUTH
    w = Directions.WEST

    return ['South', 'South', w, s, w, w, s, w]
