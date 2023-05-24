# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import sys
import copy

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def goalTest(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
        Given a state, returns available actions.
        Returns a list of actions
        """        
        util.raiseNotDefined()

    def getResult(self, state, action):
        """
        Given a state and an action, returns resulting state.
        """
        util.raiseNotDefined()

    def getCost(self, state, action):
        """
        Given a state and an action, returns step cost, which is the incremental cost 
        of moving to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

class Node:
    """
    Search node object for your convenience.

    This object uses the state of the node to compare equality and for its hash function,
    so you can use it in things like sets and priority queues if you want those structures
    to use the state for comparison.

    Example usage:
    >>> S = Node("Start", None, None, 0)
    >>> A1 = Node("A", S, "Up", 4)
    >>> B1 = Node("B", S, "Down", 3)
    >>> B2 = Node("B", A1, "Left", 6)
    >>> B1 == B2
    True
    >>> A1 == B2
    False
    >>> node_list1 = [B1, B2]
    >>> B1 in node_list1
    True
    >>> A1 in node_list1
    False
    """
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        return self.state == other.state

    def __ne__(self, other):
        return self.state != other.state

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.

    You are not required to implement this, but you may find it useful for Q5.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def iterativeDeepeningSearch(problem):
    """
    Perform DFS with increasingly larger depth. Begin with a depth of 1 and increment depth by 1 at every step.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.goalTest(problem.getStartState()))
    print("Actions from start state:", problem.getActions(problem.getStartState()))

    Then try to print the resulting state for one of those actions
    by calling problem.getResult(problem.getStartState(), one_of_the_actions)
    or the resulting cost for one of these actions
    by calling problem.getCost(problem.getStartState(), one_of_the_actions)

    """
    from util import Stack

    def DLS(startState, startPath, maxDepth):
        '''
        helper function to perform Depth-Limited Search using a stack
        '''
        visited = set()
        stack = Stack()  # Initialize the stack
        stack.push((startState, startPath, maxDepth))  # Push the initial state
        
        while not stack.isEmpty():  # While there are nodes to process
            currentState, currentPath, depth = stack.pop()  # Pop the current node
            
            if problem.goalTest(currentState):  # If this is a goal state, return the path
                return currentPath
            
            if depth > 0:  # If we can go deeper
                
                for action in problem.getActions(currentState):  # Push all possible successors into the stack
                    nextState = problem.getResult(currentState, action)
                    if nextState not in visited:
                        stack.push((nextState, currentPath + [action], depth - 1))
                        visited.add(nextState)  # Mark current node as visited
        return None  # No solution found
    
    # Initial depth
    depth = 1

    # Variable containing the current state of the agent
    startState = problem.getStartState()

    # Iterate with different depths to save memory in case of infinite search
    while True:
        path = DLS(startState, [], depth)
        if path is not None:
            return path
        depth += 1  # Increment depth by 1 and go for the next iteration

        
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    # Initializing start state
    startNode = Node(problem.getStartState(), None, None, 0)

    # Initializing priority queue
    frontier = PriorityQueue()

    # Pushing our starting node to the queue
    frontier.push(startNode, heuristic(startNode.state, problem))

    # Initializing set for visited nodes
    visited = set()

    while not frontier.isEmpty():
        node = frontier.pop()

        if problem.goalTest(node.state):
            path = []
            while node.action is not None:
                path.append(node.action)
                node = node.parent
            return path[::-1]  # Reverse the path to get it from start to goal

        if node.state not in visited:
            visited.add(node.state)
            for action in problem.getActions(node.state):
                nextNode = Node(problem.getResult(node.state, action), node, action, node.path_cost + problem.getCost(node.state, action))
                if nextNode.state not in visited:
                    costHeu = nextNode.path_cost + heuristic(nextNode.state, problem)
                    frontier.push(nextNode, costHeu)

    return []


# Abbreviations
bfs = breadthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
