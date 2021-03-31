import copy 

""" Class with the State Nodes """
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

"""testing values"""
arr1=[2,1,2,1]
arr2=[2,1,1,2]
arr3 = []
arr4 = []
n=2
m=4
arrTotal=[arr1,arr2,arr3,arr4]
completed = [0,0,0,0]

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
    for i in range(0,n+2):
        for j in range(0,n+2):
            if validMove(parent.getMatrix(),parent.getArrCompleted(),i,j) and parent.getLastPlayedCol() != i:
                newstate = Node(parent,copy.deepcopy(parent.getMatrix()),copy.deepcopy(parent.getArrCompleted()),(i,j),parent.getDepth()+1,1)
                newstate.moveBall(i,j)
                childs.append(newstate)
    return childs

"""performs a breadth first search to the problem"""

def bfs(rootnode):
    queue = []
    queue.append(rootnode)
    currNode=None

    while len(queue) > 0:
        currNode=queue[0]
        if gameOver(currNode):
            #print("\nFOUND SOLUTION\n")
            break
        else:
            childs = generateChilds(currNode)
            for child in childs:
                queue.append(child)
            queue.pop(0)
        
    return currNode

def dfs(rootnode):
    queue = []
    queue.append(rootnode)
    currNode=None
    while len(queue) > 0:
        currNode=queue[0]
        if gameOver(currNode):
            #print("\nFOUND SOLUTION\n")
            break
        else:
            childs = generateChilds(currNode)
            queue.append(childs[0])
            queue.pop(0)

    return currNode



"""returns an array with the solution path"""

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

def getHint(node):
    solution = [(node.getMatrix(),"Final Solution")]
    currNode=node
    while True:
        parent=currNode.getParent()
        if parent != None:
            solution.append((parent.getMatrix(),currNode.getLastMove()))
            currNode=parent
        else:
            break
    solution = solution[::-1]
    return solution[0][1]
        

"""bfs search functions"""
def bfsSolveBlock(rootnode):
    print("\nBFS\n")
    finalState=bfs(rootnode)
    getSolutionPath(finalState)

def dfsSolveBlock(rootnode):
    print("\nDFS\n")
    finalState=dfs(rootnode)
    getSolutionPath(finalState)
