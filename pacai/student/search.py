"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.queue import Queue
from pacai.util.priorityQueue import PriorityQueue as PQ

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:


    """

    # *** Your Code Here ***
    s = problem.successorStates(problem.startingState())
    stack = [[p, [d]] for p, d, w in problem.successorStates(problem.startingState())]
    # stack = position, list of directions
    visited = [problem.startingState()]

    while len(stack) > 0:

        n_pos, ls = stack.pop()

        visited.append(n_pos)
        if problem.isGoal(n_pos):  #if Goal found, return list of dir to goal
            return ls
        for pos, direction, weight in problem.successorStates(n_pos):
            if not (pos in visited):
                sh_copy = ls.copy()
                sh_copy.append(direction)  # update list of directions
                stack.append([pos, sh_copy])  # append tuple of position, list of dir
    return []


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """
# *** Your Code Here ***
    #queue = [(problem.startingState(), [])  ]
    queue = Queue()
    queue.push((problem.startingState(), []))
    # print(problem.successorStates(problem.startingState()))
# while goal not found and stack not empt,y
    visited = set() 

    while len(queue) > 0:

        p_state, path = queue.pop()

        if problem.isGoal(p_state):
            return path 
       
        # what do i think is happening?
        # i think bfs is propagating to the edges and stopping once it has found the 
        if not (p_state in visited):
            visited.add(p_state) 
            for state, direction, cost in problem.successorStates(p_state):
                path2 = path.copy()
                path2.append(direction)
                queue.push((state, path2))
                #print(queue)
    return []


def uniformCostSearch(problem):

    #Search the node of least total cost first.
       # *** Your Code Here ***

    #stack = [[p, [d], w] for p, d, w in problem.successorStates(problem.startingState())]
    stack = [(problem.startingState(), [], 0)]
# while goal not found and stack not empty
    visited = {}

    while len(stack) > 0:
        stack.sort(key = lambda x: x[2])

        n_pos, ls, n_cost = stack.pop(0)

        if problem.isGoal(n_pos):
            return ls

        if not (n_pos in visited) or problem.actionsCost(ls) < visited[n_pos]:
            visited[n_pos] = n_cost # problem.actionsCost(ls)

            # sorted_successors = sorted(problem.successorStates(n_pos), key = lambda x: x[2])

            for pos, direction, cost in problem.successorStates(n_pos):
                    sh_copy = ls.copy()
                    sh_copy.append(direction)
                    stack.append([pos, sh_copy, n_cost + cost])
    return []



def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    # PQ = PriorityQueueWithFunction(evaluate)
    pq = [(problem.startingState(),[], 0, 0)]
    visited = {}

    while len(pq) > 0:
        pq.sort(key = lambda x: x[3])
        # this is slow because it regenerates the cost of each value each time 
        # instead of saving it as a value of the node
        # use a node function, tell pq to sort by node value
        # sort priorityQueue by cost to get to location, cost of heuristic (A* search)
        # idea; every node in the frontier has been visited. use visited to figure out cost?

        parentState, ls, n_cost, p_h = pq.pop(0) # pop front of pq


        if problem.isGoal(parentState):
            return ls

        if not (parentState in visited) or n_cost < visited[parentState]:
            visited[parentState] = problem.actionsCost(ls)
            for state, direction, cost in problem.successorStates(parentState):
                #if not (state in visited) or problem.actionsCost(ls + [direction]) < visited[state]:
                sh_copy = ls.copy()
                sh_copy.append(direction)
                sortedVal = n_cost + cost + heuristic(state, problem)
                pq.append((state, sh_copy, n_cost + cost, sortedVal)) # 

    return []

    # *** Your Code Here ***
    raise NotImplementedError()


