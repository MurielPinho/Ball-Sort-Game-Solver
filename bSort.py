import copy 
from collections import Counter

class Node:
    """ Constructor """
    def __init__(self,parent, matrix, arrCompleted,lastMove,depth,cost):
        self.parent = parent
        self.matrix = matrix
        self.arrCompleted = arrCompleted
        self.lastMove = lastMove
        self.depth = depth
        self.cost = cost

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
        if checkCompleted(self.matrix,toCol):
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


""" returns true if a column on a given array is completed with balls of the same colour false otherwise"""

def checkCompleted(matrix,col):
    if len(set(matrix[col])) == 1 and len(matrix[col]) == m:
        return True
    else: return False

"""returns true if a given toCol fromCol move is possible given a matrix and its completed array"""

def validMove(matrix,completed,fromCol,toCol):
    if len(matrix[fromCol]) > 0 and len(matrix[toCol]) < m and fromCol != toCol and not(completed[fromCol]):
        if len(matrix[toCol]) == 0:
            return True
        elif matrix[fromCol][-1] == matrix[toCol][-1]:
            return True
        else:
            return False
    else: return False

"""returns true if a game is over, false otherwise"""

def gameOver(node):
        if node.getArrCompleted().count(1) == n:
            return True
        else: return False

"""returns an array with all the possible child states from a given parent node"""
def generateChilds(parent):
    childs=[]
    for i in range(0,n+ntubes):
        for j in range(0,n+ntubes):
            if validMove(parent.getMatrix(),parent.getArrCompleted(),i,j) and parent.getLastPlayedCol() != i:
                newstate = Node(parent,copy.deepcopy(parent.getMatrix()),copy.deepcopy(parent.getArrCompleted()),(i,j),parent.getDepth()+1,0)
                newstate.moveBall(i,j)
                childs.append(newstate)
    return childs

arr1=[3,2,1]
arr2=[2,1,3]
arr3 = [1,2,3]
arr4 = []
n=3
m=3
ntubes=1
arrTotal=[arr1,arr2,arr3,arr4]
completed = [0,0,0,0]

root = Node(None,arrTotal,completed,(-1,-1),0,0)

graph = {

}

""" generates childs for the root node """
graph[root] = generateChilds(root)


for child in graph[root]:
    graph[child]=[]

gameovers=0

while gameovers < 20:
    for key in list(graph):
        if graph[key] == [] and not(gameOver(key)):
            graph[key] = generateChilds(key)
            for childs in graph[key]:
                graph[childs] = []
        if gameOver(key):
            gameovers += 1

bfsvisited = [] # List to keep track of visited nodes.
bfsqueue = []     #Initialize a queue

def bfs(node):
  bfsvisited.append(node)
  bfsqueue.append(node)

  while bfsqueue:
    s = bfsqueue.pop(0) 

    for neighbour in graph[s]:
        if gameOver(neighbour):
            return neighbour
        elif neighbour not in bfsvisited:
            bfsvisited.append(neighbour)
            bfsqueue.append(neighbour)

#bfs search functions
def bfsSolveBlock(rootnode):
    print("\nBFS\n")
    finalState=bfs(rootnode)
    getSolutionPath(finalState)

dfsvisited = set() # Set to keep track of visited nodes.

def dfs(node,winningStates):
    if len(winningStates) == 1:
        return
    if node not in dfsvisited:
        dfsvisited.add(node)
        for neighbour in graph[node]:
            if gameOver(neighbour):
                winningStates.append(neighbour)
            dfs(neighbour,winningStates)

def dfsSolveBlock(rootnode):
    
    print("\nDFS\n")
    winningStates=[]
    dfs(root,winningStates)
    finalState=winningStates[0]
    getSolutionPath(finalState)


def getSolutionPath(node):
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

"""
bfsSolveBlock(root)

dfsSolveBlock(root)
"""
root.addCost()
print(root.getCost())

