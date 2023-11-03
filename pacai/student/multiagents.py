import random
from pacai.core import distance 
from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent

from math import e 
from math import tanh
import random
class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()
         
        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """
        
        
        successorGameState = currentGameState.generatePacmanSuccessor(action) 
        # Useful information you can extract.
        #print(type(successorGameState))
        newPosition = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        newFood = successorGameState.getFood()  
        
        food = 0

 
        ghostRange = 3 
        foodRange = 10 
        scoreRange = 100 

        maxDistance = 0
        minDistance = 10000
        foodDistances = [] 
        for y in range(len(oldFood._data)):
            for data, x in enumerate(oldFood._data[y]):
                if oldFood._data[y][x]:

                    score = distance.maze((y, x), newPosition, successorGameState)
                    if score >  maxDistance:
                        maxDistance = score
                    if score < minDistance:
                        minDistance = score

        newGhostStates = successorGameState.getGhostStates()
        distance_from_ghosts = [distance.euclidean(ghost.getNearestPosition(), newPosition) for ghost in newGhostStates]
        normGhostD = [self.normalize(distance, ghostRange) for distance in distance_from_ghosts]
        normMinDist = self.normalize(minDistance, foodRange) 
        
        newScore = currentGameState.getScore()

        normScoreChange = self.normalize(newScore, scoreRange)
 
        # in order of importance
        ghostWeight = 30  # summing up by 4
        foodWeight = 5 
        scoreWeight = 1 
         
        foodCost = int(foodWeight *self.normalize(minDistance, ghostRange ))#tanh(foodRange/(minDistance+0.1)))
        scoreCost = scoreWeight * (successorGameState.getScore() )#- currentGameState.getScore()) 
        ghostCost = int(ghostWeight * self.normalize(min(distance_from_ghosts) ,  ghostRange)) 
        print(foodCost, scoreCost, ghostCost, "result:", foodCost+scoreCost - ghostCost)
        
        return foodCost + scoreCost - ghostCost
        # +  ghostWeight * min(distance_from_ghosts) # + minDistance * foodWeight#int(ghostSum +  foodWeight * normMinDist )


        #newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]
        # *** Your Code Here ***

        #minGhostDist = min(distance_from_ghosts)

    def normalize(self, val, weight):
        # x > 0, y is between 1 and 0,
        # x == 0, y == 1
        # when weight is greater, the rate at which slope drops is decreased. . 
        # weight = 5 gives 
        w = -val/weight
        return pow(e, w)



class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs) 
    
    def getAction(self, state):
        maxQ, maxAction = self.maximize(state) 
        print("maxQ: ", maxQ, maxAction)
        if maxAction != None:
            return maxAction
        print("shouldn't run")
        return "Stop"
        #print(state.generateSuccessor(0, state.getLegalActions(0)[0]))
        # return "Stop" 

    def minimize(self, state, depth, actor_index):

        if self.getTreeDepth()  <= depth  or state.isWin() or state.isLose():
            evaluate = self.getEvaluationFunction()
            #print("evaluation", evaluate(state), "at depth", depth)
            return (evaluate(state), None) 

        minimal_quality = 999999 
        minimizing_action = None
        for action in state.getLegalActions(actor_index):
            if action == "Stop":
                pass
            newState = state.generateSuccessor(actor_index, action)
            quality = minimal_quality
            if actor_index + 1 == state.getNumAgents():
                quality, a2  = self.maximize(newState, depth + 1, 0)
            else:
                quality, a2 = self.minimize(newState, depth, actor_index + 1)
            if quality < minimal_quality:
                minimal_quality = quality
                minimizing_action = action
        # print("minimized_quality ", minimal_quality, "depth", depth, "agent", actor_index) 
        return (minimal_quality, minimizing_action)
 
    def maximize(self, state, depth=0, actor_index=0):
        if self.getTreeDepth() <= depth or state.isLose() or state.isWin():
            evaluate = self.getEvaluationFunction()
            # print("OBSERVED", evaluate(state))
            # print("evaluation", evaluate(state), "at depth", depth)

            return (evaluate(state), None)
        
        maxQ = -999999
        maxAction = None
        for action in state.getLegalActions(actor_index):
            if action == "Stop":
                pass
            newState = state.generateSuccessor(actor_index, action)
            quality, a2 = self.minimize(newState, depth , actor_index + 1)
            if quality > maxQ:
                maxQ = quality
                maxAction = action
        #print("mazimized", maxQ, "at depth", depth)
        return (maxQ, maxAction)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
    
    def getAction(self, state):
        maxQ, maxAction, a, b = self.maximize(state) 
        print("maxQ: ", maxQ, maxAction)
        if maxAction != None:
            return maxAction
        print("shouldn't run")
        return "Stop"
        #print(state.generateSuccessor(0, state.getLegalActions(0)[0]))
        # return "Stop" 

    def minimize(self, state, depth, actor_index, a = -999999, b = 999999):

        minimal_quality = 999999 
        alpha = a
        beta = b 
        minimizing_action = None

        if self.getTreeDepth()  <= depth  or state.isWin() or state.isLose():
            evaluate = self.getEvaluationFunction()
            #print("evaluation", evaluate(state), "at depth", depth)
            return (evaluate(state), None, alpha, beta) 

        for action in state.getLegalActions(actor_index):
            if action == "Stop":
                pass
            newState = state.generateSuccessor(actor_index, action)
            quality = minimal_quality
            if actor_index + 1 == state.getNumAgents():
                quality, a2, a, b  = self.maximize(newState, depth + 1, 0)
            else:
                quality, a2, a, b = self.minimize(newState, depth, actor_index + 1)
            if b < beta:
                beta = b

            if quality < minimal_quality:
                minimal_quality = quality
                minimizing_action = action

            if alpha > beta:
                break
        # print("minimized_quality ", minimal_quality, "depth", depth, "agent", actor_index) 
        return (minimal_quality, minimizing_action, alpha, beta)
 
    def maximize(self, state, depth=0, actor_index=0, a = -999999, b = 999999):
        if self.getTreeDepth() <= depth or state.isLose() or state.isWin():
            evaluate = self.getEvaluationFunction()
            # print("OBSERVED", evaluate(state))
            # print("evaluation", evaluate(state), "at depth", depth)

            return (evaluate(state), None, a, b)
        
        maxQ = -999999
        alpha = a
        beta = b
        maxAction = None
        for action in state.getLegalActions(actor_index):
            if action == "Stop":
                pass
            newState = state.generateSuccessor(actor_index, action)
            quality, a2, a, b = self.minimize(newState, depth , actor_index + 1)
            if quality > maxQ:
                maxQ = quality
                maxAction = action
            if a > alpha:
                alpha = a
            if alpha > beta:
                break
        #print("mazimized", maxQ, "at depth", depth)
        return (maxQ, maxAction, alpha, beta)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """

    return currentGameState.getScore()

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
