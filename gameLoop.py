import pygame
import copy 
from solver import *
from pygame.locals import (
    K_ESCAPE,
    K_h,
    K_s,
    KEYDOWN,
    QUIT,
)
#Colors
white = (236, 239, 241)
black = (38, 50, 56)
grey = (144, 164, 174)
red = (244, 67, 54)
green = (76, 175, 80)
blue = (33, 150, 243)
orange = (255, 152, 0)
pink = (240, 98, 146)
purple = (156, 39, 176)


levels = [
    [3,4,4,[[3,2,1],[2,1,1,2],[1,2,3],[3,3]]],
    [2,4,4,[[2,2,2,1],[1,1,1,2],[],[]]],
    [2,4,4,[[],[2,1,2,1],[1,2,1,2],[]]],
    [2,4,4,[[2,1,2,1],[],[1,2,1,2],[]]]]
    
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ball Sort Puzzle")

class Game:
    def __init__(self,level):
        self.n=levels[level][0]
        self.m=levels[level][1]
        self.ntubes=levels[level][2]
        self.arrTotal=levels[level][3]
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
        self.hint = [0,0]
        self.showHint = False
        pygame.init()
  
    def loadNextLevel(self):
        self.currentLevel = self.currentLevel + 1 
        self.game = Game(self.currentLevel)
        self.tubeSelected = False
        self.fromTube = -1
        self.toTube = -1

    def drawGame(self):
        font = pygame.font.Font('freesansbold.ttf', 32)      
        screen.fill(white)
        level = font.render('Level', True, black)
        screen.blit(level,(100,30))
        levelText = font.render("%d" % (self.currentLevel + 1), True, black)
        screen.blit(levelText,(137,70))         
        hint = font.render('Hint', True, black)
        screen.blit(hint,(600,30))

        if self.showHint:
            hintText = font.render("%d -> %d" % tuple(self.hint), True, black)
            screen.blit(hintText,(590,70))    

        for x  in range(0,self.game.m):
            self.drawTube(x)    
       

    def color(self,number):
        if number == 1:
            color = red
        elif number == 2:
            color = green
        elif number == 3:
            color = blue
        elif number == 4:
            color = orange
        elif number == 5:
            color = pink
        elif number == 6:
            color = purple
        return color

    def drawTube(self,number):
        center = SCREEN_WIDTH / (self.game.m+1)
        tube = pygame.Surface((60, 300)) 
        font = pygame.font.Font('freesansbold.ttf', 40)
        tube.fill(black)
        if number == self.fromTube:
            tube.fill(grey)
        tube_center = ((center*(number+1) -tube.get_width()/2),(SCREEN_HEIGHT-tube.get_height())/2 + 30)
        pygame.draw.rect(tube,white,pygame.Rect(5,0,50,215))
        pygame.draw.rect(tube,white,pygame.Rect(0,220,60,80))  
        text = font.render("%d" % number, True, black, white)
        tube.blit(text,(20,240))
        currentBall = 1
        for x in self.game.arrTotal[number]:    
            pygame.draw.circle(tube,self.color(x),(30,215-(25*currentBall)),20)
            currentBall = currentBall +2
        tubeClickable = screen.blit(tube, tube_center)
        self.game.tubesArray[number] = tubeClickable

    def handleMouseClick(self):
        pos=pygame.mouse.get_pos()
        for tube in self.game.tubesArray:
            if tube.collidepoint(pos):
                if not self.tubeSelected : 
                    self.fromTube = self.game.tubesArray.index(tube)
                    self.tubeSelected = True
                else:
                    self.toTube = self.game.tubesArray.index(tube)
                    self.game.moveBall(self.fromTube,self.toTube)
                    self.tubeSelected = False
                    self.fromTube = -1 
                    self.toTube = -1 
                    self.showHint = False
    
    def updateHint(self):
        self.showHint = True
        root = Node(None,self.game.arrTotal,self.game.completed,self.game.n,self.game.m,self.game.ntubes,(-1,-1),0,0)
        graph1 = Graph(root)
        self.hint = graph1.getHint(root)
        

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                self.handleMouseClick()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                elif event.key == K_h:
                    self.updateHint()
                elif event.key == K_s:
                    root = Node(None,self.game.arrTotal,self.game.completed,self.game.n,self.game.m,self.game.ntubes,(-1,-1),0,0)
                    graph1 = Graph(root)
                    graph1.bfsSolveBlock(root)
                    graph1.dfsSolveBlock(root)

                    
            elif event.type == QUIT:
                return False
        return True

    def update(self):
        self.drawGame()
        pygame.display.flip()
        if self.game.gameOver():
            if self.currentLevel < len(levels)-1:
                self.loadNextLevel()
            else:
                return False
        return True