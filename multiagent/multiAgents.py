#ILYES_BAALI_AI_HW2

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        #print "Legal Moves: ",legalMoves

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        #print "Scores: ",scores
        bestScore = max(scores)
        #print "Best Score: ",bestScore
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

        if successorGameState.isWin():
          return 3000 # arbitrarly big number, it set by trail and error

        GhostsPosition = successorGameState.getGhostPositions()
        distToGhosts = [util.manhattanDistance(ghostposition, newPos) for ghostposition in GhostsPosition]
        mindistToGhost = min(distToGhosts)**0.5
        
        lessfood =0
        stop =0
        if (currentGameState.getNumFood() > successorGameState.getNumFood()):
            lessfood = 1
        if action == Directions.STOP:
            stop = 1
        foodlist = newFood.asList()
        initDistTofood = 100
        distTofood = min([util.manhattanDistance(foodpos, newPos) for foodpos in foodlist])

        score = mindistToGhost + 50*lessfood - 5*stop - distTofood
        return successorGameState.getScore() + score

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
        """
        "*** YOUR CODE HERE ***"
       

        bestScore,bestMove=self.maxFunction(gameState,self.depth)

        return bestMove

    def maxFunction(self,gameState,depth):
        if depth==0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "Stop"

        moves=gameState.getLegalActions()
        scores = [self.minFunction(gameState.generateSuccessor(0,move),1, depth) for move in moves]
        bestScore=max(scores)
        bestIndices = [index for index in xrange(len(scores)) if scores[index] == bestScore]
        chosenIndex = bestIndices[0]
        return bestScore,moves[chosenIndex]

    def minFunction(self,gameState,agent, depth):  
        if depth==0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "Stop"

        moves=gameState.getLegalActions(agent) #get legal actions.
        #scores=[]
        if(agent!=gameState.getNumAgents()-1):
          scores =[self.minFunction(gameState.generateSuccessor(agent,move),agent+1,depth) for move in moves]
        else:
          scores =[self.maxFunction(gameState.generateSuccessor(agent,move),(depth-1)) for move in moves]
        minScore=min(scores)
        worstIndices = [index for index in range(len(scores)) if scores[index] == minScore]
        chosenIndex = worstIndices[0]
        return minScore, moves[chosenIndex]

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
        alpha = -(float("inf"))
        beta = float("inf")
        score,bestmove=self.maxFunction(gameState,self.depth, alpha, beta)

        return bestmove

    def maxFunction(self,gameState,depth, alpha, beta):
        if depth==0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "Stop"

        moves=gameState.getLegalActions()
        v  = -(float("inf"))
        bestmove = Directions.STOP
        for move in moves:
          prevscore = v
          v = max(v,self.minFunction(gameState.generateSuccessor(0,move),1, depth,alpha, beta)[0])
          if v > beta:
            return v, bestmove
          alpha = max(alpha, v)
          if v > prevscore:
            bestmove = move
            
        
        return v,bestmove

    def minFunction(self,gameState,agent, depth, alpha, beta):  
        if depth==0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "Stop"

        moves=gameState.getLegalActions(agent) #get legal actions.
        score  = float("inf")
        bestmove = Directions.STOP
        if(agent!=gameState.getNumAgents()-1):
          for move in moves:
            prevscore = score
            score = min(score,self.minFunction(gameState.generateSuccessor(agent,move),agent+1,depth,alpha, beta)[0])
            if score < alpha:
                  return score, bestmove
            if score < prevscore:
              bestmove = move
            beta = min(beta, score)

          #scores =[self.minFunction(gameState.generateSuccessor(agent,move),agent+1,depth,alpha, beta) for move in moves]
        else:
          #scores =[self.maxFunction(gameState.generateSuccessor(agent,move),(depth-1),alpha, beta)[0] for move in moves]
          for move in moves:
            prevscore = score
            score = min(score,self.maxFunction(gameState.generateSuccessor(agent,move),(depth-1),alpha, beta)[0])
            if score < alpha:
              return score, bestmove
            beta = min(beta, score)
            if score < prevscore:
              bestmove = move
            beta = min(beta, score)
            
        return score, bestmove
        util.raiseNotDefined()
import inspect
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
        bestScore,bestMove=self.maxFunction(gameState,self.depth)

        return bestMove

    def maxFunction(self,gameState,depth):
        if depth==0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "Stop"

        moves=gameState.getLegalActions()
        scores = [self.minFunction(gameState.generateSuccessor(0,move),1, depth)[0] for move in moves]
        bestScore=max(scores)
        bestIndices = [index for index in xrange(len(scores)) if scores[index] == bestScore]
        chosenIndex = bestIndices[0]
        return bestScore,moves[chosenIndex]

    def minFunction(self,gameState,agent, depth): 
        if depth==0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "Stop"

        #get legal actions.
        moves=gameState.getLegalActions(agent) 

        NumMoves = float(len(moves))

        score = float("inf")

        if(agent!=gameState.getNumAgents()-1):
          score =sum([self.minFunction(gameState.generateSuccessor(agent,move),agent+1,depth)[0]/NumMoves for move in moves])
        
        else:
          score =sum([self.maxFunction(gameState.generateSuccessor(agent,move),(depth-1))[0]/NumMoves for move in moves])
        
        return score, "Stop"


        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    if currentGameState.isWin():
          return 3000 # arbitrarly big number
    elif currentGameState.isLose(): 
         return -3000 # arbitrarly small number

    pos = currentGameState.getPacmanPosition()

    # food distance
    foodlist = currentGameState.getFood().asList()

    distTofood = min([util.manhattanDistance(pos, food) for food in foodlist])    

    numberOfCapsulesLeft = len(currentGameState.getCapsules())
    
    
    numberOfFoodsLeft = len(foodlist)
    
    scaredGhosts = []
    
    for ghost in currentGameState.getGhostStates():
      if ghost.scaredTimer: 
        scaredGhosts.append(ghost)

    mindistToScaredGhost = 0
      
    if scaredGhosts:
      mindistToScaredGhost = min([util.manhattanDistance(pos, ghostposition.getPosition()) for ghostposition in scaredGhosts])
    
    return scoreEvaluationFunction(currentGameState) - distTofood + \
             - 2*mindistToScaredGhost  - 20*numberOfCapsulesLeft - 4*numberOfFoodsLeft

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

