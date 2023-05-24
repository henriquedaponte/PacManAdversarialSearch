# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 7)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        _, action = self.minimax(gameState, 0, self.depth)

        return action

    def minimax(self, gameState, agentIndex, depth):
        # If it's pacman's turn
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depth)
        # If it's ghost's turn
        else:
            return self.minValue(gameState, agentIndex, depth)

    def maxValue(self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState), None

        value = -float('inf')
        action = None
        for a in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, a)
            newValue, _ = self.minimax(successorGameState, (agentIndex + 1) % gameState.getNumAgents(), depth - 1 if (agentIndex + 1) % gameState.getNumAgents() == 0 else depth)
            if newValue > value:
                value, action = newValue, a

        return value, action

    def minValue(self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState), None

        value = float('inf')
        action = None
        for a in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, a)
            newValue, _ = self.minimax(successorGameState, (agentIndex + 1) % gameState.getNumAgents(), depth - 1 if (agentIndex + 1) % gameState.getNumAgents() == 0 else depth)
            if newValue < value:
                value, action = newValue, a

        return value, action
   
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 8)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        _, action = self.expectimax(gameState, 0, self.depth)
        return action
    
    def expectimax(self, gameState, agentIndex, depth):
        # If it's pacman's turn
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depth)
        # If it's ghost's turn
        else:
            return self.expValue(gameState, agentIndex, depth)

    def maxValue(self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState), None

        value = -float('inf')
        action = None
        for a in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, a)
            newValue, _ = self.expectimax(successorGameState, (agentIndex + 1) % gameState.getNumAgents(), depth - 1 if (agentIndex + 1) % gameState.getNumAgents() == 0 else depth)
            if newValue > value:
                value, action = newValue, a

        return value, action

    def expValue(self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState), None

        value = 0
        legalActions = gameState.getLegalActions(agentIndex)
        prob = 1.0 / len(legalActions)
        for a in legalActions:
            successorGameState = gameState.generateSuccessor(agentIndex, a)
            newValue, _ = self.expectimax(successorGameState, (agentIndex + 1) % gameState.getNumAgents(), depth - 1 if (agentIndex + 1) % gameState.getNumAgents() == 0 else depth)
            value += newValue * prob

        return value, None


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 9).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    # Compute distance to the nearest food
    foodDist = [manhattanDistance(newPos, food) for food in newFood.asList()]
    minFoodDist = min(foodDist) if foodDist else 1

    # Compute distance to the nearest ghost
    ghostDist = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]
    minGhostDist = min(ghostDist) if ghostDist else 1

    # Compute the number of remaining food
    numFood = currentGameState.getNumFood()

    # Compute the number of remaining capsules
    numCapsules = len(currentGameState.getCapsules())

    # Compute the scared time of the nearest ghost
    minScaredTime = min(newScaredTimes) if newScaredTimes else 0

    # Take into account the current game score
    score = currentGameState.getScore()

    # Compute the final evaluation score
    score += 1.0 / minFoodDist
    if minGhostDist > minScaredTime:
        score -= 1.0 / minGhostDist if minGhostDist else 1
    else:
        score += 1.0 / minGhostDist if minGhostDist else 1 # encourage Pacman to eat the scared ghost
    score -= 2 * numFood
    score -= 2 * numCapsules  # encourage Pacman to eat the capsule

    return score




# Abbreviation
better = betterEvaluationFunction

