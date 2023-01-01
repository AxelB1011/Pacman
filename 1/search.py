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

from operator import truediv
import util

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

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    #if the start state is a goal state, we dont need to do anything
    if problem.isGoalState(start):
        return []
    #dfs uses Stack
    frontier = util.Stack()
    visited = []
    node = (start, [], 0)
    #initialize search tree(frontier) using the initial problem state
    frontier.push(node)
    #while there are no candidates for expansion
    while not frontier.isEmpty():
        #state, action, cost
        currS, currA, currC = frontier.pop()
        #add to visited list if we havent visited before
        if currS not in visited:
            visited.append(currS)
            #return current list of actions if current state is goal state
            if  problem.isGoalState(currS):
                return currA
            else:
                #expand nodes and add the resulting nodes to search tree(frontier)
                succs = problem.getSuccessors(currS)
                for s, a, c in succs:
                    newA = currA + [a]
                    newC = currC + c
                    newN = (s, newA, newC)
                    frontier.push(newN)
    return currA
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    #if the start state is a goal state, we dont need to do anything
    if problem.isGoalState(start):
        return []
    #bfs uses Queue
    frontier = util.Queue()
    visited = []
    node = (start, [], 0)
    #initialize search tree(frontier) using the initial problem state
    frontier.push(node)
    #while there are no candidates for expansion
    while not frontier.isEmpty():
        #state, action, cost
        currS, currA, currC = frontier.pop()
         #add to visited list if we havent visited before
        if currS not in visited:
            visited.append(currS)
            #return current list of actions if current state is goal state
            if  problem.isGoalState(currS):
                return currA
            else:
                #expand nodes and add the resulting nodes to search tree(frontier)
                succs = problem.getSuccessors(currS)
                for s, a, c in succs:
                    newA = currA + [a]
                    newC = currC + c
                    newN = (s, newA, newC)
                    frontier.push(newN)
    return currA
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    #if the start state is a goal state, we dont need to do anything
    if problem.isGoalState(start):
        return []
    #UCS(Dijkstra's) uses a Priority Queue(PQ) with path cost
    frontier = util.PriorityQueue()
    visited = {} #state : cost
    node = (start, [], 0)
    #initialize search tree(frontier) using the initial problem state and cost
    frontier.push(node, 0) #state, cost
    #while there are no candidates for expansion
    while not frontier.isEmpty():
        #state, action, cost
        currS, currA, currC = frontier.pop()
        #add to visited dict if we havent visited before 
        #or update path cost if currrent Cost is less than the stored cost for the current state
        if currS not in visited or currC < visited[currS]:
            visited[currS] = currC
            #return current list of actions if current state is goal state
            if  problem.isGoalState(currS):
                return currA
            else:
                #expand nodes and add the resulting nodes to search tree(frontier)
                succs = problem.getSuccessors(currS)
                for s, a, c in succs:
                    newA = currA + [a]
                    newC = currC + c
                    newN = (s, newA, newC)
                    frontier.update(newN, newC)
    return currA
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    #if the start state is a goal state, we dont need to do anything
    if problem.isGoalState(start):
        return []
    #A* also uses a PQ with path cost like UCS
    frontier = util.PriorityQueue()
    visited = [] #state : cost
    node = (start, [], 0)
    #initialize search tree(frontier) using the initial problem state and cost
    frontier.push(node, 0) #state, cost
    #while there are no candidates for expansion
    while not frontier.isEmpty():
        #state, action, cost
        currS, currA, currC = frontier.pop()
        #add to visited list
        visited.append((currS, currC))
        #return current list of actions if current state is goal state
        if  problem.isGoalState(currS):
                return currA
        else:
            #expand nodes and add the resulting nodes to search tree(frontier)
            succs = problem.getSuccessors(currS)
            for s, a, c in succs:
                newA = currA + [a]
                newC = problem.getCostOfActions(newA)
                newN = (s, newA, newC)
                #flag to check if successor has already been visited
                flag = False
                for v in visited:
                    st, ct = v
                    if(s==st and newC>=ct):
                        flag = True
                #if successor not in visited then push to PQ/update existing value in PQ and add to visited
                if not flag:
                    frontier.update(newN, newC+heuristic(s, problem))
                    visited.append((s, newC))
                    
    return currA
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch