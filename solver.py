import copy 
from collections import Counter

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

class Node:
    """ Constructor """
    def __init__(self,parent, matrix, arrCompleted, n, m, ntubes, lastMove, depth, cost):
        self.parent = parent
        self.matrix = matrix
        self.arrCompleted = arrCompleted
        self.lastMove = lastMove
        self.depth = depth
        self.cost = cost
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
    def getCost(self):
        return self.cost
    
    """ Returns Node parent """
    def getParent(self):
        return self.parent
    
    """ moves a ball in nodes matrix """
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
    def addCost(self):
        for column in self.matrix:
            numCount = Counter(column)
            if len(column) > 1:
                for common in numCount.most_common(1):
                    commonNumber = common[0]
                for i in range(0,len(column)):
                    if column[i] == commonNumber:
                        continue
                    else:
                        self.cost+=(len(column)-i)
                        break
            elif len(column)==1: self.cost += 1
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
        if len(self.matrix[fromCol]) > 0 and len(self.matrix[toCol]) < self.m and fromCol != toCol and not(self.arrCompleted[fromCol]):
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
                x,y = self.getLastMove()
                if self.validMove(i,j) and i!=y:
                    newstate = Node(self,copy.deepcopy(self.getMatrix()),copy.deepcopy(self.getArrCompleted()),self.n,self.m,self.ntubes,(i,j),self.getDepth()+1,0)
                    newstate.moveBall(i,j)
                    childs.append(newstate)
        return childs

class Graph:
    def __init__(self,root):
        self.root = root
        self.graph = {}
        self.bfsvisited = [] # List to keep track of visited nodes.
        self.bfsqueue = []
        self.bfscounter=0 
        self.dfscounter=0
        self.dfsvisited = set()
        

    def bfs(self,node):
        self.graph = {}
        self.bfsvisited.append(node.getMatrix())
        self.bfsqueue.append(node)
        

        while self.bfsqueue:
            s = self.bfsqueue.pop(0)
            
            if s.gameOver():
                    return s
            self.graph[s] = s.generateChilds()

            for neighbour in self.graph[s]:
                self.bfscounter+=1
                if neighbour.getMatrix() not in self.bfsvisited:
                    self.bfsvisited.append(neighbour.getMatrix())
                    self.bfsqueue.append(neighbour)


    def depthFirst(self,initState):
        visited = []
        states = Stack()
        states.push(initState)
        while not states.isEmpty() :

            visited.append(states.peek().getMatrix())
            newChildren = states.peek().generateChilds()
            newChildren.reverse()
            states.pop()

            for child in newChildren:
                if child.gameOver():
                    return child
                elif child.getMatrix() not in visited:
                    self.dfscounter+=1
                    states.push(child)

    def limitedDepthSearch(self, initState,limit):
        visited = []
        states = Stack()
        states.push([initState,0])
        while not states.isEmpty() :

          
            value = states.peek()[1] + 1
            if value > limit:
                states.pop()
                continue

            visited.append(states.peek()[0].getMatrix())
            newChildren = states.peek()[0].generateChilds()
            newChildren.reverse()
            states.pop()

            for child in newChildren:
                if child.gameOver():
                    return child
                elif child.getMatrix() not in visited:
                    self.dfscounter+=1
                    states.push([child,value])
        
    def depthSolveBlock(self,rootnode,limit):
        
        print("\nLimited Depth\n")
        finalState = self.limitedDepthSearch(rootnode,limit)    
        print("\nLimited Depth\n","Number of states expanded = ",self.dfscounter)
        self.getSolutionPath(finalState)
    def dfsSolveBlock(self,rootnode):
        
        print("\nDFS\n")
        winningStates=[]
        finalState = self.depthFirst(rootnode)
        
        print("\nDFS\n","Number of states expanded = ",self.dfscounter)
        self.getSolutionPath(finalState)
        
    def bfsSolveBlock(self,rootnode):
        finalState=self.bfs(rootnode)
        print("\nBFS\n","Number of states expanded = ",self.bfscounter)
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
        for step in reversed(solution):
            print(step[0]," Next move (from,to):" ,step[1])
    
    def solve(self,rootnode,solver):
        if solver == 1:
            solution = self.bfs(rootnode)
        else:
            solution = self.bfs(rootnode)
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

arrTotal=[[2,2,2,1],[1,1,1,2],[]]
completed = [0,0,0,0]

root = Node(None,arrTotal,completed,2,4,3,(-1,-1),0,0)

graph1 = Graph(root)
graph1.dfsSolveBlock(root)


# print(root.getCost())

