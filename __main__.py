import os, sys
import pygame
from pygame.locals import *

pygame.init()

#Set the window
SURFACE = pygame.display.set_mode((640,480))
#Set the window title
pygame.display.set_caption('Deeper')

#We need a set FPS for animations
FPS = 30
FPS_CLOCK = pygame.time.Clock()


def start() :
    global LEVELS, LEVEL_INDEX
    LEVELS = parse_level_file('levels.txt')
    LEVEL_INDEX = 0

    while True:
        result = play_level()

        if result == 'caught' :
            pass
        elif result == 'succeeded' :
            pass


def play_level() :
        global CURRENT_IMAGE
        CURRENT_LEVEL = LEVELS[ LEVEL_INDEX ]

        # MAP = # ...
        # Handle all events here
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        #update the display
        pygame.display.update()
        #Wait a tick to draw the next frame
        fpsClock.tick(FPS)

def parse_level_file(filename) :
    assert os.path.exists(filename), "Cannot find the level file: %s" % (filename)

    map_file = open(filename, 'r')

    contents = map_file.readlines() + ['\r\n']
    map_file.close()

    levels = []
    level_number = 0
    level_text_lines = []
    map = []

    for i in range(len(contents)) :
        # Current line, without linebreaks
        line = contents[i].rstrip('\r\n')

        # Ignore everything after comments
        if ';' in line :
            line = line[:line.find(';')]

        if line != '' : # Current line is a part of the map
            level_text_lines.append(line)
        elif line == '' and len(level_text_lines) > 0 :
            # Find the longest row in the map
            # Add spaces to the end of shorter lines to ensure that the content is rectangular.
            # Convert level_text_lines to a level object
            pass

if __name__ == '__main__':
    start()
