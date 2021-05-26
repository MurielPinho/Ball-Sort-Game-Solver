import copy 
from collections import Counter

class Node:
    """ Constructor """
    def __init__(self,parent, matrix, arrCompleted, n, m, ntubes, lastMove, depth, evaluatedValue):
        self.parent = parent
        self.matrix = matrix
        self.arrCompleted = arrCompleted
        self.lastMove = lastMove
        self.depth = depth
        self.evaluatedValue = evaluatedValue
        self.n = n
        self.m = m
        self.ntubes = ntubes

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
    def moveBall(self,fromCol,toCol):
        num = self.matrix[fromCol].pop(-1)
        self.matrix[toCol].append(num)
        if self.checkCompleted(self.matrix,toCol):
            self.arrCompleted[toCol] = 1
        self.lastMove = (fromCol,toCol)

    """ Prints Node matrix """
    def printNode(self):
        print("\nMatrix\n")
        print(self.matrix)
    
    """evaluates the state matrix and gives it a cost, lower is better"""
    def evaluateState(self):
        for column in self.matrix:
            numCount = Counter(column)
            if len(column) > 1:
                for common in numCount.most_common(1):
                    commonNumber = common[0]
                for i in range(0,len(column)):
                    if column[i] == commonNumber:
                        continue
                    else:
                        self.evaluatedValue+=((len(column)-i)*1)
                        break
            elif len(column)==1: self.evaluatedValue += 1

    """returns true if a game is over, false otherwise"""

    def gameOver(self):
            if self.getArrCompleted().count(1) == self.n:
                return True
            else: return False

    """ returns true if a column on a given array is completed with balls of the same colour false otherwise"""

    def checkCompleted(self,matrix,col):
        if len(set(matrix[col])) == 1 and len(matrix[col]) == self.m:
            return True
        else: return False

    """returns true if a given toCol fromCol move is possible given a matrix and its completed array"""

    def validMove(self,fromCol,toCol):
        if len(self.matrix[fromCol]) > 0 and len(self.matrix[toCol]) < self.m and fromCol != toCol:
            if len(self.matrix[toCol]) == 0:
                return True
            elif self.matrix[fromCol][-1] == self.matrix[toCol][-1]:
                return True
            else:
                return False
        else: return False



    """returns an array with all the possible child states from a given parent node"""
    def generateChilds(self):
        childs=[]
        for i in range(0,self.ntubes):
            for j in range(0,self.ntubes):
                y = self.getLastMove()
                if self.validMove(i,j) and i!=y[1]:
                    newstate = Node(self,copy.deepcopy(self.getMatrix()),copy.deepcopy(self.getArrCompleted()),self.n,self.m,self.ntubes,(i,j),self.getDepth()+1,0)
                    newstate.moveBall(i,j)
                    newstate.evaluateState()
                    childs.append(newstate)
        return childs

class Graph:
    def __init__(self,root):
        self.root = root
        self.statesCounter=1 
        

    def breadthFirst(self,node):
        
        visited = []
        states = []
        states.append(node)
        visited.append(node.getMatrix())
        self.statesCounter = 1

        while states:
            state=states.pop(0)     
            children = state.generateChilds()
            for child in children:         
                if child.getMatrix() not in visited:
                        self.statesCounter += 1
                        visited.append(child.getMatrix())
                        states.append(child)
        return visited

    

    def depthFirst(self,initState):
        visited = []
        states = []
        states.append(initState)
        self.statesCounter = 1

        while not len(states) == 0 :

            visited.append(states[-1].getMatrix())
            newChildren = states[-1].generateChilds()
            newChildren.reverse()
            states.pop()

            for child in newChildren:
                if child.gameOver():
                    return child
                elif child.getMatrix() not in visited:
                    self.statesCounter+=1
                    states.append(child)

    def limitedDepthSearch(self, initState,limit):
        visited = []
        states = []
        states.append([initState,0])
        self.statesCounter = 1

        while not len(states) == 0 :

          
            value = states[-1][1] + 1
            if value > limit:
                states.pop()
                continue

            visited.append(states[-1][0].getMatrix())
            newChildren = states[-1][0].generateChilds()
            newChildren.reverse()
            states.pop()

            for child in newChildren:
                if child.gameOver():
                    return child
                elif child.getMatrix() not in visited:
                    self.statesCounter+=1
                    states.append([child,value])

    def progressiveDeepening(self, initState, progress):

        currentProgress = progress
        visited = []
        toBeChecked = []
        states = []
        states.append([initState, 0])
        self.statesCounter = 1


        while True:

            if len(states) == 0:
                currentProgress += progress
                toBeChecked.reverse()
                for i in toBeChecked:
                    states.append(i)
                toBeChecked = []

            if states[-1][1] == currentProgress and states[-1][1] != 0:
                toBeChecked.append(states[-1])
                states.pop()
                continue

            visited.append(states[-1][0].getMatrix())
            newChildren = states[-1][0].generateChilds()
            newChildren.reverse()
            value = states[-1][1] + 1
            states.pop()

            for newChild in newChildren:

                if newChild.gameOver():
                    return newChild
                elif newChild.getMatrix() not in visited:
                    self.statesCounter+=1
                    states.append([newChild, value])

    def uniformCostSearch(self, initState):

        visited = []
        states = []
        states.append([initState, initState.getEvaluatedValue()])
        visited.append(initState.getMatrix())
        self.statesCounter = 1

        while states:
            states.sort(key=lambda x: x[1])
            state = states.pop(0)
            children = state[0].generateChilds()
            for child in children:
                if child.getMatrix() not in visited:
                    if child.gameOver():
                        return child
                    else:
                        self.statesCounter += 1
                        visited.append(child.getMatrix())
                        states.append([child,child.getDepth()])

    def greedySearch(self, initState):

        visited = []
        states = []
        states.append([initState, initState.getEvaluatedValue()])
        visited.append(initState.getMatrix())
        self.statesCounter = 1

        while states:
            states.sort(key=lambda x:x[1])
            
            state = states.pop(0)
            
            children = state[0].generateChilds()
            for child in children:
                if child.getMatrix() not in visited:
                    if child.gameOver():
                        return child
                    else:
                        self.statesCounter += 1
                        visited.append(child.getMatrix())
                        states.append([child,child.getEvaluatedValue()])
    
    def aStarSearch(self, initState):

        visited = []
        states = []
        states.append([initState, initState.getEvaluatedValue()+initState.getDepth()])
        visited.append(initState.getMatrix())
        self.statesCounter = 1

        while states:
            states.sort(key=lambda x: x[1])
            state = states.pop(0)
            children = state[0].generateChilds()
            for child in children:
                if child.getMatrix() not in visited:
                    if child.gameOver():
                        return child
                    else:
                        self.statesCounter += 1
                        visited.append(child.getMatrix())
                        states.append(
                            [child, (child.getEvaluatedValue()*5)+child.getDepth()])
                        

        
    def limitedDepthSolveBlock(self,rootnode,limit):
        finalState = self.limitedDepthSearch(rootnode,limit)    
        print("\nLimited Depth\n", "Number of states -> ",
              self.statesCounter, " \n Number of moves  -> ", finalState.getDepth())
        self.getSolutionPath(finalState)

    def iterativeSolveBlock(self,rootnode,progress):
        finalState = self.progressiveDeepening(rootnode,progress)    
        print("\nIterative Deepening\n", "Number of states -> ",
              self.statesCounter, " \n Number of moves  -> ", finalState.getDepth())
        self.getSolutionPath(finalState)

    def depthSolveBlock(self,rootnode):
        finalState = self.depthFirst(rootnode)
        print("\nDepth First Search\n", "Number of states -> ",
              self.statesCounter, " \n Number of moves  -> ", finalState.getDepth())
        self.getSolutionPath(finalState)
        
    def breadthSolveBlock(self,rootnode):
        finalState=self.breadthFirst(rootnode)
        result = []
        for state in range(0,300):
            print(state,": ")
            for col in finalState[state]:
                if(len(col) < 4):
                    for i in range(len(col),4):
                        col.append(0)
            result.append(finalState[state])
            print(finalState[state],",\n")

                    
    
    def uniformSolveBlock(self,rootnode):
        finalState = self.uniformCostSearch(rootnode)
        print("\nUniform Cost Search\n", "Number of states -> ",
              self.statesCounter, " \n Number of moves  -> ", finalState.getDepth())
        self.getSolutionPath(finalState)

    def greedySolveBlock(self,rootnode):
        finalState = self.greedySearch(rootnode)
        print("\nGreedy Search\n", "Number of states -> ",
              self.statesCounter, " \n Number of moves  -> ", finalState.getDepth())
        self.getSolutionPath(finalState)

    def aStarSolveBlock(self,rootnode):
        finalState = self.aStarSearch(rootnode)
        print("\nA* Search\n", "Number of states -> ",
              self.statesCounter, " \n Number of moves  -> ", finalState.getDepth())
        self.getSolutionPath(finalState)

    def getSolutionPath(self,node):
        solution = [(node.getMatrix(),"Final Solution")]
        currNode=node
        while True:
            parent=currNode.getParent()
            if parent != None:
                solution.append((parent.getMatrix(),currNode.getLastMove()))
                currNode=parent
            else:
                break
        # for step in reversed(solution):
        #     print(step[0]," Next move (from,to):" ,step[1])
    
    def solve(self,rootnode,solver):
        if solver == 1:
            solution = self.aStarSearch(rootnode)
        if solver == 2:
            solution = self.greedySearch(rootnode)
        if solver == 3:
            solution = self.depthFirst(rootnode)
        else:
            solution = self.aStarSearch(rootnode)
        return solution

    def getHint(self,rootnode,solver):
        node=self.solve(rootnode,solver)
        solution = [(node.getMatrix(),"Final Solution")]
        currNode=node
        while True:
            parent=currNode.getParent()
            if parent != None:
                solution.append((parent.getMatrix(),currNode.getLastMove()))
                currNode=parent
            else:
                break
        return solution[-1][1]


