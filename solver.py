import copy 
from collections import Counter

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
    
    def getLastPlayedCol(self):
        return self.lastMove[1]
    
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
                if self.validMove(i,j) and self.getLastPlayedCol() != i:
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
        self.dfsvisited = set()
        self.generateGraph()

    """ generates childs for the root node """
    def generateGraph(self):
        
        gameovers=0
        self.graph[self.root] = self.root.generateChilds()
    
        for child in self.graph[self.root]:
            self.graph[child]=[]
        
        while gameovers < 20:
            for key in list(self.graph):
                if self.graph[key] == [] and not(key.gameOver()):
                    self.graph[key] = key.generateChilds()
                    for childs in self.graph[key]:
                        self.graph[childs] = []
                if key.gameOver():
                    gameovers += 1

    def bfs(self,node):
        self.bfsvisited.append(node)
        self.bfsqueue.append(node)

        while self.bfsqueue:
            s = self.bfsqueue.pop(0) 

            for neighbour in self.graph[s]:
                if neighbour.gameOver():
                    return neighbour
                elif neighbour not in self.bfsvisited:
                    self.bfsvisited.append(neighbour)
                    self.bfsqueue.append(neighbour)

    def dfs(self,node,winningStates):
        if len(winningStates) == 1:
            return
        if node not in self.dfsvisited:
            self.dfsvisited.add(node)
            for neighbour in self.graph[node]:
                if neighbour.gameOver():
                    winningStates.append(neighbour)
                self.dfs(neighbour,winningStates)

    def dfsSolveBlock(self,rootnode):
        
        print("\nDFS\n")
        winningStates=[]
        self.dfs(rootnode,winningStates)
        finalState=winningStates[0]
        self.getSolutionPath(finalState)
    def bfsSolveBlock(self,rootnode):
        print("\nBFS\n")
        finalState=self.bfs(rootnode)
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
    

    def getHint(self,rootnode):
        node=self.bfs(rootnode)
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




arrTotal=[[3,2,1],[2,1,1,2],[1,2,3],[3,3]]
completed = [0,0,0,0]

root = Node(None,arrTotal,completed,3,4,4,(-1,-1),0,0)

graph1 = Graph(root)
graph1.bfsSolveBlock(root)
graph1.dfsSolveBlock(root)

# root.addCost()
# print(root.getCost())

