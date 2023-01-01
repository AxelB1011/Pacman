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

"""
Gopal Krishna Shukla
U10076283
"""

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
        scoreDiff, dir, pos = successorGameState.getScore() - currentGameState.getScore(), currentGameState.getPacmanState().getDirection(), currentGameState.getPacmanPosition()
        
        nearestFood = min([manhattanDistance(pos, i) for i in currentGameState.getFood().asList()])
        nearestSuccFood = min([manhattanDistance(newPos, i) for i in newFood.asList()]) if [manhattanDistance(newPos, i) for i in newFood.asList()] else 0 #min() arg is empty error
        foodDiff = nearestFood - nearestSuccFood
        nearestGhost = min([manhattanDistance(newPos, i.getPosition()) for i in newGhostStates])
        if nearestGhost<=2 or action==Directions.STOP: #bad if ghost is nearby 
            return 0
        if scoreDiff > 0: #best if there is positive score difference
            return 10
        elif foodDiff > 0: #better if there is positive food difference
            return 7
        elif action==dir: #good if action is same as direction
            return 4
        else:
            return 1
        #return successorGameState.getScore()

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
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

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
    Your minimax agent (question 2)
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        v = float("-inf")
        nextA = Directions.STOP
        for a in gameState.getLegalActions(0):
            t = self.minVal(gameState.generateSuccessor(0, a), 0, 1)
            if t>v and a!=Directions.STOP:
                v = t
                nextA = a
        return nextA
    #ghosts will use minVal
    def minVal(self, state, depth, agentIndex):
        if depth==self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        else:
            actions = state.getLegalActions(agentIndex)
            val = float("inf") if len(actions)>0 else self.evaluationFunction(state)
            for a in actions:
                if agentIndex==state.getNumAgents()-1: #last agent
                    s = self.maxVal(state.generateSuccessor(agentIndex, a), depth+1, 0)
                    val = min(val, s)
                else:
                    s = self.minVal(state.generateSuccessor(agentIndex, a), depth, agentIndex+1)
                    val = min(val, s)
            return val
    #pacman will use maxVal
    def maxVal(self, state, depth, agentIndex):
        if depth==self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        else:
            actions = state.getLegalActions(agentIndex)
            val = float("-inf") if len(actions)>0 else self.evaluationFunction(state)
            for a in actions:
                s = self.minVal(state.generateSuccessor(agentIndex, a), depth, agentIndex+1)
                val = max(val, s)
            return val
    
        util.raiseNotDefined()
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        v = float("-inf")
        nextA = Directions.STOP
        alpha, beta = float("-inf"), float("inf")
        for a in gameState.getLegalActions(0):
            t = self.minVal(gameState.generateSuccessor(0, a), 0, 1, alpha, beta)
            if t>v and a!=Directions.STOP:
                v = t
                nextA = a
            if t>beta:
                return nextA
            alpha = max(alpha, t)
        return nextA
        #util.raiseNotDefined()

    
    def minVal(self, state, depth, agentIndex, alpha, beta):
        if depth==self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        else:
            actions = state.getLegalActions(agentIndex)
            val = float("inf") if len(actions)>0 else self.evaluationFunction(state)
            for a in actions:
                if agentIndex==state.getNumAgents()-1:
                    val = min(val, self.maxVal(state.generateSuccessor(agentIndex, a), depth+1, 0, alpha, beta))
                    if val<alpha:
                        return val
                    beta = min(val, beta)
                else:
                    val = min(val, self.minVal(state.generateSuccessor(agentIndex, a), depth, agentIndex+1, alpha, beta))
                    if val<alpha:
                        return val
                    beta = min(val, beta)
            return val

    def maxVal(self, state, depth, agentIndex, alpha, beta):
        if depth==self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        else:
            actions = state.getLegalActions(0)
            val = float("-inf") if len(actions)>0 else self.evaluationFunction(state)
            for a in actions:
                val = max(val, self.minVal(state.generateSuccessor(0, a), depth, 1, alpha, beta))
                if val>beta:
                    return val
                alpha = max(val, alpha)
            return val
    

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        v = float("-inf")
        nextA = Directions.STOP
        alpha, beta = float("-inf"), float("inf")
        for a in gameState.getLegalActions(0):
            t = self.expVal(gameState.generateSuccessor(0, a), 0, 1)
            if t>v and a!=Directions.STOP:
                v = t
                nextA = a
        return nextA
        #util.raiseNotDefined()
    def maxVal(self, state, depth, agentIndex):
        if depth==self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        else:
            actions = state.getLegalActions(0)
            val = float("-inf") if len(actions)>0 else self.evaluationFunction(state)
            for a in actions:
                val = max(val, self.expVal(state.generateSuccessor(0, a), depth, 1))
            return val

    def expVal(self, state, depth, agentIndex):
        if depth==self.depth or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        else:
            actions = state.getLegalActions(agentIndex)
            val = float("inf") if len(actions)>0 else self.evaluationFunction(state)
            p = 0
            for a in actions:
                if agentIndex==state.getNumAgents()-1:
                    val = self.maxVal(state.generateSuccessor(agentIndex, a), depth+1, 0)
                else:
                    val = self.expVal(state.generateSuccessor(agentIndex, a), depth, agentIndex+1)
                p += val
            return float(p)/float(len(actions))

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <Calculates manhattan dist to nearest food and uses that value(inverse) along with current score to evaluate states>
    """
    "*** YOUR CODE HERE ***"
    pos, food, v = currentGameState.getPacmanPosition(), currentGameState.getFood(), currentGameState.getScore()
    nearestFood = min([manhattanDistance(pos, i) for i in food.asList()]) if [manhattanDistance(pos, i) for i in food.asList()] else 0.1 #div by 0 error
    ans = (1/nearestFood)+v #simple inverse relation
    return ans
    util.raiseNotDefined()
    

# Abbreviation
better = betterEvaluationFunction
