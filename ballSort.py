import pygame

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

arr1=[2,1,2,1]
arr2=[1,2,1,2]
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
        else: return False
    else: return False

def moveBall(fromCol,toCol):
    if validMove(fromCol,toCol):
        num = arrTotal[fromCol].pop(-1)
        arrTotal[toCol].append(num)
        fillCompleted(toCol)
    else:print("Invalid Move!")

def gameOver():
    if completed.count(1) == n:
        return True
    else: return False

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

def drawMap():
    screen.fill((236, 239, 241))
    for x  in range(1,nTubes):
        drawTube(x)
 
def color(number):
    if number == 1:
        color = (244, 67, 54)
    elif number == 2:
        color = (76, 175, 80)
    elif number == 3:
        color = (33, 150, 243)
    elif number == 4:
        color = (255, 152, 0)
    elif number == 5:
        color = (255, 193, 7)
    elif number == 6:
        color = (156, 39, 176)
    return color

def drawTube(number):
    center = SCREEN_WIDTH / nTubes
    tube = pygame.Surface((60, 220))
    tube.fill((38, 50, 56))
    if number == fromTube:
        tube.fill((144, 164, 174))
    tube_center = (
    (center*number -tube.get_width()/2),
    (SCREEN_HEIGHT-tube.get_height())/2
    )
    pygame.draw.rect(tube,(236, 239, 241),pygame.Rect(5,0,50,215))
    currentBall = 1
    for x in arrTotal[number-1]:    
        pygame.draw.circle(tube,color(x),(30,215-(25*currentBall)),20)
        currentBall = currentBall +2
    tubeClickable = screen.blit(tube, tube_center)
    tubesArray[number-1] = tubeClickable

## Game 
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
running = True
tubeSelected = False
fromTube = -1
toTube = -1
tubesArray = [0]*m
nTubes = len(arrTotal)+1 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos=pygame.mouse.get_pos()
            for tube in tubesArray:
                if tube.collidepoint(pos):
                    if not tubeSelected : 
                        fromTube = tubesArray.index(tube)+1
                        tubeSelected = True
                    else:
                        toTube = tubesArray.index(tube)+1
                        moveBall(fromTube-1,toTube-1)
                        tubeSelected = False
                        fromTube = -1 
                        toTube = -1 
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    
    drawMap()
    pygame.display.flip()
    if gameOver():
        running= False
pygame.quit()


