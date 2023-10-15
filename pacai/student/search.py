"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""
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
    queue = [[p, [d], w] for p, d, w in problem.successorStates(problem.startingState())]
    # print(problem.successorStates(problem.startingState()))
# while goal not found and stack not empty
    visited = {problem.startingState()}

    while len(queue) > 0:

        p_state, path, cost = queue.pop(0)
        #print("test")
        if problem.isGoal(p_state):
            return path 
        visited.add(p_state)
        # what do i think is happening?
        # i think bfs is propagating to the edges and stopping once it has found the 
        for state, direction, cost in problem.successorStates(p_state):
            if not (state in visited):
                path2 = path.copy()
                path2.append(direction)
                queue.append([state, path2, cost + 1])
    return []


def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """    # *** Your Code Here ***

    stack = [[p, [d], w] for p, d, w in problem.successorStates(problem.startingState())]
# while goal not found and stack not empty
    visited = {problem.startingState(): 0}

    while len(stack) > 0:
        stack.sort(key = lambda x: x[2])

        n_pos, ls, n_cost = stack.pop(0)

        visited[n_pos] = problem.actionsCost(ls)
        if problem.isGoal(n_pos):
            return ls
        sorted_successors = sorted(problem.successorStates(n_pos), key = lambda x: x[2])

        for pos, direction, cost in sorted_successors:
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

    pq = [[p, [d], w] for p, d, w in problem.successorStates(problem.startingState())]
    visited = {problem.startingState(): 0}

    while len(pq) > 0:
        pq.sort(key = lambda x: problem.actionsCost(x[1]) + heuristic(x[0], problem))
        # sort priorityQueue by cost to get to location, cost of heuristic (A* search)

        n_pos, ls, n_cost = pq.pop(0) # pop front of pq

        visited[n_pos] = problem.actionsCost(ls)
        if problem.isGoal(n_pos):
            return ls

        for pos, direction, cost in problem.successorStates(n_pos):
            if not (pos in visited) or problem.actionsCost(ls + [direction]) < visited[pos]:
                sh_copy = ls.copy()
                sh_copy.append(direction)
                pq.append([pos, sh_copy, problem.actionsCost(sh_copy)])

    return []

    # *** Your Code Here ***
    raise NotImplementedError()
