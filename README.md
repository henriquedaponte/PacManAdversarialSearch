# PacManAdversarialSearch
Implemented search algorithms (Astar, IDS) for PacMan to navigate through a maze environment and then adversarial search algorithms (Minimax, Expectimax) for PacMan to beat the ghosts with an average score higher than 1000

code forked from http://ai.berkeley.edu/project_overview.html

Files edited:
search.py
searchAgents.py
multiAgents.py


Functions and Classes implemented:

def iterativeDeepeningSearch(problem):
- Perform DFS with increasingly larger depth. Begin with a depth of 1 and increment depth by 1 at every step.
- Returns a list of actions that reaches the goal.

def aStarSearch(problem, heuristic=nullHeuristic):
- Implemented A* search with user choice's heuristic to find optimal path

class CornersProblem(search.SearchProblem):
- Created a search problem to check efficiency for A* search
- This search problem finds paths through all four corners of a layout.

cornersHeuristic(state, problem):
- Created a custom heuristic function for CornersProblem
- Based on manhattan distance

class MinimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

    def minimax(self, gameState, agentIndex, depth):
    - Minimax function
    - If pacman's turn, max value
    - if ghosts turn, min value

    def maxValue(self, gameState, agentIndex, depth):
    - Calculates the action that will bring max value to Pacman

    def minValue(self, gameState, agentIndex, depth):
    - Calculate action expected from ghost that will minimize value to pacman
    
 class ExpectimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
    def expectimax(self, gameState, agentIndex, depth):
    def maxValue(self, gameState, agentIndex, depth):
    def expValue(self, gameState, agentIndex, depth):
    
def betterEvaluationFunction(currentGameState):
- extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.
       
