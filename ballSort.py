arr1=[2,2,2,1]
arr2=[1,1,1,2]
arr3 = []
arr4 = []
n=2
m=4
arrTotal=[arr1,arr2,arr3,arr4]
completed = [0]*m


def fillCompleted(col):
    if checkCompleted(col):
        completed[col] = 1

def checkCompleted(col):
    if len(set(arrTotal[col])) == 1 and len(arrTotal[col]) == m:
        return True
    else: return False

def validMove(fromCol,toCol):
    if len(arrTotal[fromCol]) > 0 and len(arrTotal[toCol]) < m and fromCol != toCol and not(completed[fromCol]):
        if len(arrTotal[toCol]) == 0:
            return True
        elif arrTotal[fromCol][-1] == arrTotal[toCol][-1]:
            return True
        else:
            return False
    else: return False

def moveBall(fromCol,toCol):
    if validMove(fromCol,toCol):
        num = arrTotal[fromCol].pop(-1)
        arrTotal[toCol].append(num)
        fillCompleted(toCol)
    else:print("Move Invalid!")

def gameOver():
    if completed.count(1) == n:
        print("Game Over")
    else: print("Not Over")


class Node:
    def __init__(self, matrix, arrCompleted,lastMove):
        self.matrix = matrix
        self.arrCompleted = arrCompleted
        self.lastMove = lastMove

    def printNode(self):
        print("\nMatrix\n")
        print(self.matrix)
        print("\nCompleted\n")
        print(self.arrCompleted)
        print("\nLast Move\n")
        print(self.lastMove)

N1 = Node(arrTotal,completed,-1)
N1.printNode()


