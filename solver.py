import copy
import time
from collections import Counter


class Node:
<<<<<<< HEAD
    """ Constructor """

    def __init__(self, parent, matrix, arrCompleted, n, m, ntubes, lastMove, depth, evaluatedValue):
=======
   #Constructor 
    def __init__(self,parent, matrix, arrCompleted, n, m, ntubes, lastMove, depth, evaluatedValue):
>>>>>>> 127be939caa535ca1867f1d08648c779391b95ed
        self.parent = parent
        self.matrix = matrix
        self.arrCompleted = arrCompleted
        self.lastMove = lastMove
        self.depth = depth
        self.evaluatedValue = evaluatedValue
        self.n = n
        self.m = m
        self.ntubes = ntubes

<<<<<<< HEAD
    """ Returns Node matrix """

    def getMatrix(self):
        return self.matrix

    """ Returns Node completed array """

    def getArrCompleted(self):
        return self.arrCompleted

    """ Returns Node's parent move """

    def getLastMove(self):
        return self.lastMove

    """ Returns Node Depth """

    def getDepth(self):
        return self.depth

    """ Returns Node Cost """

    def getEvaluatedValue(self):
        return self.evaluatedValue

    """ Returns Node parent """

    def getParent(self):
        return self.parent

    """ moves  a ball in nodes matrix """

    def moveBall(self, fromCol, toCol):
=======
    #Returns Node matrix
    def getMatrix(self):
        return self.matrix
    
    #Returns Node completed array 
    def getArrCompleted(self):
        return self.arrCompleted
    
    #Returns Node's parent move 
    def getLastMove(self):
        return self.lastMove
    
    #Returns Node Depth 
    def getDepth(self):
        return self.depth
    
    #Returns Node Cost
    def getEvaluatedValue(self):
        return self.evaluatedValue
    
    #Returns Node parent
    def getParent(self):
        return self.parent
    
    #moves  a ball in nodes matrix
    def moveBall(self,fromCol,toCol):
>>>>>>> 127be939caa535ca1867f1d08648c779391b95ed
        num = self.matrix[fromCol].pop(-1)
        self.matrix[toCol].append(num)
        if self.checkCompleted(self.matrix, toCol):
            self.arrCompleted[toCol] = 1
        self.lastMove = (fromCol, toCol)

<<<<<<< HEAD
    """ Prints Node matrix """

    def printNode(self):
        print("\nMatrix\n")
        print(self.matrix)

    """evaluates the state matrix and gives it a cost, lower is better"""

=======
    #Prints Node matrix
    def printNode(self):
        print("\nMatrix\n")
        print(self.matrix)
    
    #evaluates the state based on expected number of moves needed to reach objective state -> smaller eval is better
>>>>>>> 127be939caa535ca1867f1d08648c779391b95ed
    def evaluateState(self):
        for column in self.matrix:
            numCount = Counter(column)
            if len(column) > 1:
                for common in numCount.most_common(1):
                    commonNumber = common[0]
                for i in range(0, len(column)):
                    if column[i] == commonNumber:
                        continue
                    else:
                        self.evaluatedValue += ((len(column) - i) * 1)
                        break
            elif len(column) == 1:
                self.evaluatedValue += 1

 #evaluates the state based on number of same coloured balls from bottom to top in each column -> bigger eval is better
    def evaluateState2(self):
        for column in self.matrix:
            if len(column) == 0:
                continue
            else:
                num = column[0]
            for i in range(0, len(column)):
                if column[i] == num:
                    self.evaluatedValue += 1
                else:
                    break

    #returns true if a game is over, false otherwise

    def gameOver(self):
        if self.getArrCompleted().count(1) == self.n:
            return True
        else:
            return False

    #returns true if a column on a given array is completed with balls of the same colour false otherwise

    def checkCompleted(self, matrix, col):
        if len(set(matrix[col])) == 1 and len(matrix[col]) == self.m:
            return True
        else:
            return False

    #returns true if a given toCol fromCol move is possible given a matrix and its completed array

    def validMove(self, fromCol, toCol):
        if len(self.matrix[fromCol]) > 0 and len(self.matrix[toCol]) < self.m and fromCol != toCol and not (
        self.arrCompleted[fromCol]):
            if len(self.matrix[toCol]) == 0:
                return True
            elif self.matrix[fromCol][-1] == self.matrix[toCol][-1]:
                return True
            else:
                return False
        else:
            return False

<<<<<<< HEAD
    """returns an array with all the possible child states from a given parent node"""

    def generateChilds(self, heuristic):
        childs = []
        for i in range(0, self.ntubes):
            for j in range(0, self.ntubes):
=======
    #returns an array with all the possible child states from a given parent node
    def generateChilds(self,heuristic):
        childs=[]
        for i in range(0,self.ntubes):
            for j in range(0,self.ntubes):
>>>>>>> 127be939caa535ca1867f1d08648c779391b95ed
                y = self.getLastMove()
                if self.validMove(i, j) and i != y[1]:
                    newstate = Node(self, copy.deepcopy(self.getMatrix()), copy.deepcopy(self.getArrCompleted()),
                                    self.n, self.m, self.ntubes, (i, j), self.getDepth() + 1, 0)
                    newstate.moveBall(i, j)
                    if heuristic == 1:
                        newstate.evaluateState()
                    elif heuristic == 2:
                        newstate.evaluateState2()
                    childs.append(newstate)
        return childs


class Graph:
    def __init__(self, root):
        self.root = root
        self.statesCounter = 1
        self.startTime = 0
        self.endTime = 0
<<<<<<< HEAD

    def breadthFirst(self, node):

=======
        
#breadth first search algoritm
    def breadthFirst(self,node):
        
>>>>>>> 127be939caa535ca1867f1d08648c779391b95ed
        visited = []
        states = []
        states.append(node) #append root
        visited.append(node.getMatrix()) #append root matrix state 
        self.statesCounter = 1
        self.startTime = time.time()

        while states:
<<<<<<< HEAD
            state = states.pop(0)
            children = state.generateChilds(None)
            for child in children:
=======
            state=states.pop(0)   #pops first element in the queue
            children = state.generateChilds(None) #generates it's possible child states
            for child in children:         
>>>>>>> 127be939caa535ca1867f1d08648c779391b95ed
                if child.getMatrix() not in visited:
                    if child.gameOver():
                        self.endTime = time.time()
                        return child  #found solution
                    else:
                        self.statesCounter += 1
                        visited.append(child.getMatrix())
                        states.append(child)

    def depthFirst(self, initState):
        visited = []
        states = []
        states.append(initState) #append root
        self.statesCounter = 1
        self.startTime = time.time();

        while not len(states) == 0:

            visited.append(states[-1].getMatrix())
            children = states[-1].generateChilds(None)
            children.reverse()
            states.pop()

            for child in children:
                if child.gameOver():
                    self.endTime = time.time();
                    return child
                elif child.getMatrix() not in visited:
                    self.statesCounter += 1
                    states.append(child)

    def limitedDepthSearch(self, initState, limit):
        visited = []
        states = []
        states.append([initState, 0])
        self.statesCounter = 1
        self.startTime = time.time()

        while not len(states) == 0:

            value = states[-1][1] + 1
            if value > limit:
                states.pop()
                continue

            visited.append(states[-1][0].getMatrix())
            children = states[-1][0].generateChilds(None)
            children.reverse()
            states.pop()

            for child in children:
                if child.gameOver():
                    self.endTime = time.time()
                    return child
                elif child.getMatrix() not in visited:
                    self.statesCounter += 1
                    states.append([child, value])

    def progressiveDeepening(self, initState, progress):

        currentProgress = progress
        visited = []
        toBeChecked = []
        states = []
        states.append([initState, 0])
        self.statesCounter = 1
        self.startTime = time.time()

        while True:

            if len(states) == 0:
                currentProgress += progress
                toBeChecked.reverse()
                for i in toBeChecked:
                    states.append(i)
                toBeChecked = []
            if not states:
                return
            if states[-1][1] == currentProgress and states[-1][1] != 0:
                toBeChecked.append(states[-1])
                states.pop()
                continue

            visited.append(states[-1][0].getMatrix())
            children = states[-1][0].generateChilds(None)
            children.reverse()
            value = states[-1][1] + 1
            states.pop()

            for child in children:

                if child.gameOver():
                    self.endTime = time.time()
<<<<<<< HEAD
                    return newChild
                elif newChild.getMatrix() not in visited:
                    self.statesCounter += 1
                    states.append([newChild, value])
=======
                    return child
                elif child.getMatrix() not in visited:
                    self.statesCounter+=1
                    states.append([child, value])
>>>>>>> 127be939caa535ca1867f1d08648c779391b95ed

    def uniformCostSearch(self, initState):

        visited = []
        states = []
        states.append([initState, initState.getEvaluatedValue()])
        visited.append(initState.getMatrix())
        self.statesCounter = 1
        self.startTime = time.time()

        while states:
            states.sort(key=lambda x: x[1])
            state = states.pop(0)
            children = state[0].generateChilds(None)
            for child in children:
                if child.getMatrix() not in visited:
                    if child.gameOver():
                        self.endTime = time.time()
                        return child
                    else:
                        self.statesCounter += 1
                        visited.append(child.getMatrix())
                        states.append([child, child.getDepth()])

    def greedySearch(self, initState, heuristic):

        visited = []
        states = [[initState, initState.getEvaluatedValue()]]
        visited.append(initState.getMatrix())
        self.statesCounter = 1
        self.startTime = time.time()

        while states:

            states.sort(key=lambda x: x[1])
            if heuristic == 2:
                states.reverse()

            state = states.pop(0)
            children = state[0].generateChilds(heuristic)

            for child in children:
                if child.getMatrix() not in visited:
                    if child.gameOver():
                        self.endTime = time.time()
                        return child
                    else:
                        self.statesCounter += 1
                        visited.append(child.getMatrix())
                        states.append([child, child.getEvaluatedValue()])

    def aStarSearch(self, initState, heuristic):

        visited = []
        states = [[initState, initState.getEvaluatedValue() + initState.getDepth()]]
        visited.append(initState.getMatrix())
        self.statesCounter = 1
        self.startTime = time.time()

        while states:
            states.sort(key=lambda x: x[1])
            if heuristic == 2:
                states.reverse()
            state = states.pop(0)

            children = state[0].generateChilds(heuristic)
            for child in children:
                if child.getMatrix() not in visited:
                    if child.gameOver():
                        self.endTime = time.time()
                        return child
                    else:
                        self.statesCounter += 1
                        visited.append(child.getMatrix())
                        states.append(
                            [child, (child.getEvaluatedValue() * 5) + child.getDepth()])

    def limitedDepthSolveBlock(self, rootnode, limit):
        finalState = self.limitedDepthSearch(rootnode, limit)
        if not finalState:
            print("Limited Depth: No solutions!")
            return
        print("\nLimited Depth\n", "Number of states -> ",
              self.statesCounter, " \n Number of moves  -> ", finalState.getDepth(),
              "\nElapsed Time : ", self.endTime - self.startTime, " seconds"
              )
        self.getSolutionPath(finalState)

    def iterativeSolveBlock(self, rootnode, progress):
        finalState = self.progressiveDeepening(rootnode, progress)
        if not finalState:
            print("Iterative deepening: No solutions!")
            return
        print("\nIterative Deepening\n", "Number of states -> ",
              self.statesCounter, " \n Number of moves  -> ", finalState.getDepth(),
              "\nElapsed Time : ", self.endTime - self.startTime, " seconds")
        self.getSolutionPath(finalState)

    def depthSolveBlock(self, rootnode):
        finalState = self.depthFirst(rootnode)
        if not finalState:
            print("DFS: No solutions!")
            return
        print("\nDepth First Search\n", "Number of states -> ",
              self.statesCounter, " \n Number of moves  -> ", finalState.getDepth(),
              "\nElapsed Time : ", self.endTime - self.startTime, " seconds")
        self.getSolutionPath(finalState)

    def breadthSolveBlock(self, rootnode):
        finalState = self.breadthFirst(rootnode)
        if not finalState:
            print("BFS: No solutions!")
            return
        print("\nBreadth First Search\n", "Number of states -> ",
              self.statesCounter, " \n Number of moves  -> ", finalState.getDepth(),
              "\nElapsed Time : ", self.endTime - self.startTime, " seconds")
        self.getSolutionPath(finalState)

    def uniformSolveBlock(self, rootnode):
        finalState = self.uniformCostSearch(rootnode)
        if not finalState:
            print("Uniform Cost: No solutions!")
            return
        print("\nUniform Cost Search\n", "Number of states -> ",
              self.statesCounter, " \n Number of moves  -> ", finalState.getDepth(),
              "\nElapsed Time : ", self.endTime - self.startTime, " seconds")
        self.getSolutionPath(finalState)

    def greedySolveBlock(self, rootnode, heuristic):
        finalState = self.greedySearch(rootnode, heuristic)
        if not finalState:
            print("Greedy: No solutions!")
            return
        print("\nGreedy Search\n", "Number of states -> ",
              self.statesCounter, " \n Number of moves  -> ", finalState.getDepth(),
              "\nElapsed Time : ", self.endTime - self.startTime, " seconds", "\nHeuristic -> ", heuristic)
        self.getSolutionPath(finalState)

    def aStarSolveBlock(self, rootnode, heuristic):
        finalState = self.aStarSearch(rootnode, heuristic)
        if not finalState:
            print("A*: No solutions!")
            return
        print("\nA* Search\n", "Number of states -> ",
              self.statesCounter, " \n Number of moves  -> ", finalState.getDepth(),
              "\nElapsed Time : ", self.endTime - self.startTime, " seconds", "\nHeuristic -> ", heuristic)
        self.getSolutionPath(finalState)

    def getSolutionPath(self, node):
        solution = [(node.getMatrix(), "Final Solution")]
        currNode = node
        while True:
            parent = currNode.getParent()
            if parent != None:
                solution.append((parent.getMatrix(), currNode.getLastMove()))
                currNode = parent
            else:
                break
            return solution
        # for step in reversed(solution):
        #     print(step[0]," Next move (from,to):" ,step[1])

    def solve(self, rootnode, solver):
        if solver == 1:
            solution = self.aStarSearch(rootnode, 1)
        if solver == 2:
            solution = self.greedySearch(rootnode, 1)
        if solver == 3:
            solution = self.depthFirst(rootnode)
        if solver == 4:
            solution = self.breadthFirst(rootnode)
        if solver == 5:
            solution = self.uniformCostSearch(rootnode)
        if solver == 6:
            solution = self.progressiveDeepening(rootnode , 5)
        if solver == 7:
            solution = self.limitedDepthSearch(rootnode,30)
        else:
            solution = self.aStarSearch(rootnode, 1)
        return solution

    def getHint(self, rootnode, solver):
        node = self.solve(rootnode, solver)
        if not node:
            return -1
        solution = [(node.getMatrix(), "Final Solution")]
        currNode = node
        while True:
            if not currNode:
                return -1
            parent = currNode.getParent()
            if parent != None:
                solution.append((parent.getMatrix(), currNode.getLastMove()))
                currNode = parent
            else:
                break
        return solution[-1][1]

    def getAutoSolve(self, rootnode, solver):
        node = self.solve(rootnode, solver)
        solution = []
        currNode = node
        while True:
            if not currNode:
                return []
            parent = currNode.getParent()
            if parent != None:
                solution.append((parent.getMatrix(), currNode.getLastMove()))
                currNode = parent
            else:
                break
        return solution
