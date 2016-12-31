"*** YOUR CODE HERE ***"
       

        bestScore,bestMove=self.maxFunction(gameState,self.depth)

        return bestMove

    def maxFunction(self,gameState,depth):
        if depth==0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "noMove"

        moves=gameState.getLegalActions()
        scores = [self.minFunction(gameState.generateSuccessor(0,move),1, depth) for move in moves]
        bestScore=max(scores)
        bestIndices = [index for index in xrange(len(scores)) if scores[index] == bestScore]
        chosenIndex = bestIndices[0]
        return bestScore,moves[chosenIndex]

    def minFunction(self,gameState,agent, depth):  
        if depth==0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "noMove"

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