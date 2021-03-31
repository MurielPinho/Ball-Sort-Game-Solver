import pygame
from solver import *
from pygame.locals import (
    K_ESCAPE,
    K_h,
    KEYDOWN,
    QUIT,
)

levels = [
    [2,4,[[2,1,2,1],[1,2,1,2],[],[]]],
    [2,4,[[2,2,2,1],[1,1,1,2],[],[]]],
    [2,4,[[],[2,1,2,1],[1,2,1,2],[]]],
    [2,4,[[2,1,2,1],[],[1,2,1,2],[]]]]
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Game:
    def __init__(self,level):
        self.n=levels[level][0]
        self.m=levels[level][1]
        self.arrTotal=levels[level][2]
        self.completed = [0]*self.m
        self.tubesArray = [0]*self.m

    def fillCompleted(self,col):
        if self.checkCompleted(col):
            self.completed[col] = 1

    def checkCompleted(self,col):
        if len(set(self.arrTotal[col])) == 1 and len(self.arrTotal[col]) == self.m:
            return True
        else: return False

    def validMove(self,fromCol,toCol):
        if len(self.arrTotal[fromCol]) > 0 and len(self.arrTotal[toCol]) < self.m and fromCol != toCol and not(self.completed[fromCol]):
            if len(self.arrTotal[toCol]) == 0:
                return True
            elif self.arrTotal[fromCol][-1] == self.arrTotal[toCol][-1]:
                return True
            else: return False
        else: return False

    def moveBall(self,fromCol,toCol):
        if self.validMove(fromCol,toCol):
            num = self.arrTotal[fromCol].pop(-1)
            self.arrTotal[toCol].append(num)
            self.fillCompleted(toCol)
        else:print("Invalid Move!")

    def gameOver(self):
        if self.completed.count(1) == self.n:
            return True
        else: return False

class gameLoop:
    def __init__(self):
        self.game = Game(0)
        self.tubeSelected = False
        self.fromTube = -1
        self.toTube = -1
        self.currentLevel = 0
        pygame.init()
  
    def loadNextLevel(self):
        self.currentLevel = self.currentLevel + 1 
        self.game = Game(self.currentLevel)
        self.tubeSelected = False
        self.fromTube = -1
        self.toTube = -1

    def drawMap(self):
        screen.fill((236, 239, 241))
        for x  in range(1,self.game.m+1):
            self.drawTube(x)
    
    def color(self,number):
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

    def drawTube(self,number):
        center = SCREEN_WIDTH / (self.game.m+1)
        tube = pygame.Surface((60, 220))
        tube.fill((38, 50, 56))
        if number == self.fromTube:
            tube.fill((144, 164, 174))
        tube_center = (
        (center*number -tube.get_width()/2),
        (SCREEN_HEIGHT-tube.get_height())/2
        )
        pygame.draw.rect(tube,(236, 239, 241),pygame.Rect(5,0,50,215))
        currentBall = 1
        for x in self.game.arrTotal[number-1]:    
            pygame.draw.circle(tube,self.color(x),(30,215-(25*currentBall)),20)
            currentBall = currentBall +2
        tubeClickable = screen.blit(tube, tube_center)
        self.game.tubesArray[number-1] = tubeClickable

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos=pygame.mouse.get_pos()
                for tube in self.game.tubesArray:
                    if tube.collidepoint(pos):
                        if not self.tubeSelected : 
                            self.fromTube = self.game.tubesArray.index(tube)+1
                            self.tubeSelected = True
                        else:
                            self.toTube = self.game.tubesArray.index(tube)+1
                            self.game.moveBall(self.fromTube-1,self.toTube-1)
                            self.tubeSelected = False
                            self.fromTube = -1 
                            self.toTube = -1 
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                elif event.key == K_h:
                    root = Node(None,self.game.arrTotal,self.game.completed,(-1,-1),0,1)
                    bfsSolveBlock(root)
                    dfsSolveBlock(root)
                    
            elif event.type == QUIT:
                return False
        return True

    def update(self):
        self.drawMap()
        pygame.display.flip()
        if self.game.gameOver():
            if self.currentLevel < len(levels)-1:
                self.loadNextLevel()
            else:
                return False
        return True