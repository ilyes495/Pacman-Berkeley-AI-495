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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    stack  = util.Stack() # stack for searshing the graph
    visited = [] # Keep track of visited nodes
    start =problem.getStartState() # The start node
    stack.push((start, []))  # the sart state and empty path list is pushed to the stack
    
    while stack:
        (vrtx, path) = stack.pop() # Pop tfrom the stack , vrtx: the poped node for expantion.
        if vrtx not in visited:    # if the node is visited alraedy 
            if problem.isGoalState(vrtx):
                return [p[1] for p in path]
            visited.append(vrtx)
            for successor  in problem.getSuccessors(vrtx):
                stack.push((successor[0], path+[successor]))
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    queue  = util.Queue() # queue for searshing the graph
    visited = [] # keep track of visited nodes
    start =problem.getStartState() # The start node
    queue.push((start, [])) # the sart state and empty path list is pushed to the queue
    
    while queue:
        (vrtx, path) = queue.pop()
        if vrtx not in visited: 
            if problem.isGoalState(vrtx):
                return [p[1] for p in path]
            visited.append(vrtx)
            for successor in problem.getSuccessors(vrtx) :
                queue.push((successor[0], path+[successor]))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    queue  = util.PriorityQueue() # PrioritQueue for searshing the graph/ it expand the node with the lowest cost
    visited = [] # Keep track of visited nodes
    path = [] # Keep track of  the path
    start =problem.getStartState() # The start node

    queue.push((start, path,0), 0) 
   
    while  not queue.isEmpty():
        (vrtx, path, costparent) = queue.pop() 
        if vrtx not in visited: 
            if problem.isGoalState(vrtx):
                return [p[1] for p in path]

            visited.append(vrtx)       
            for successor in problem.getSuccessors(vrtx):
                    cost = successor[2]+ costparent
                    queue.push((successor[0], path+[successor],cost),cost)
                    

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
    queue  = util.PriorityQueue() # PriorityQueue for searshing the graph, priorityqueue helps to pop the element with the lowest priority (cost)
    visited = [] # cKepp track of visited nodes
    path = [] # Keep track of  the path
    start =problem.getStartState() # The start node
  
    queue.push((start, path,0), 0) # we push (vertex, path , cost from parent to the vertex), 
                                    #priority(which is the cost of getting to the vertex)
   
    while  not queue.isEmpty():
        (vrtx, path, costparent) = queue.pop() 
        if vrtx not in visited: 
            if problem.isGoalState(vrtx):
                return [p[1] for p in path] # return the actions
            visited.append(vrtx)    
            for successor in problem.getSuccessors(vrtx):
                    gn = successor[2]+ costparent # the real cost from root to the expanded node(successor).
                    fn = gn+heuristic(successor[0], problem) # the heursitic from the expanded node to the goal node.
                    queue.push((successor[0], path+[successor],gn),fn)# push the noe with f(n) as the priority element.
    
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
