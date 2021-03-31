from gameLoop import *

running = True
gameLoop = gameLoop()

while running:
    if not gameLoop.handleEvents():
        running = False
    if not gameLoop.update():
        running = False