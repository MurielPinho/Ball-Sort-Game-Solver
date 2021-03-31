import copy 

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

arr1=[1,2,3]
arr2=[2,1,3]
arr3 = [3,2,1]
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

def bfs(visited, graph, node):
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

"""bfs search functions"""
def bfsSolveBlock(rootnode):
    print("\nBFS\n")
    finalState=bfs(visited,graph,rootnode)
    getSolutionPath(finalState)

bfsSolveBlock(root)
