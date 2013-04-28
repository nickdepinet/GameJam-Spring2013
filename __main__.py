import os, sys
import pygame
from pygame.locals import *

pygame.init()

#Set the window
gameSurface = pygame.display.set_mode((640,480))
#Set the window title
pygame.display.set_caption('Deeper')

#We need a set FPS for animations
FPS = 30
fpsClock = pygame.time.Clock()

#main loop
while True:
    for event in pygame.event.get():
        #Quit event
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    #update the display
    pygame.display.update()
    #Wait a tick to draw the next frame
    fpsClock.tick(FPS)
    
