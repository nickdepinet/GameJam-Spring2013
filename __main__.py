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

# Directions
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

#Some Constants to Use
TILE_HEIGHT = 64
TILE_WIDTH = 64
BGCOLOR = (255,0,255)

def start() :
    global LEVELS, LEVEL_INDEX, SPRITES, LEVEL_MAP
    LEVELS = parse_level_file('levels.txt')
    LEVEL_INDEX = 0
    #Sprite Map
    SPRITES = {'wall':pygame.image.load('Images/wall.png'),
            'player':pygame.image.load('Images/player.png'),
            'floor':pygame.image.load('Images/floor.png')}
    #Floor Map
    LEVEL_MAP = {'#':SPRITES['wall'],
            ' ':SPRITES['floor']}

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
            # KeyPress, check which key it is
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a):
                    direction = LEFT
                elif (event.key == K_DOWN or event.key == K_s):
                    direction = DOWN
                elif (event.key == K_UP or event.key == K_w):
                    direction = UP
                elif (event.key == K_RIGHT or event.key == K_d):
                    direction = RIGHT
                elif (event.key == K_p):
                    #Pause
                    pass
                elif (event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

        SURFACE.fill(BGCOLOR)
        #drawMap()
        #update the display
        pygame.display.update()
        #Wait a tick to draw the next frame
        FPS_CLOCK.tick(FPS)

def parse_level_file(filename) :
    assert os.path.exists(filename), "Cannot find the level file: %s" % (filename)

    map_file = open(filename, 'r')

    contents = map_file.readlines() + ['\r\n']
    map_file.close()

    levels = []
    level_number = 0
    map_text_lines = []
    map = []

    for line_number in range(len(contents)) :
        # Current line, without linebreaks
        line = contents[line_number].rstrip('\r\n')

        # Ignore everything after comments
        if ';' in line :
            line = line[:line.find(';')]

        if line != '' : # Current line is a part of the map
            map_text_lines.append(line)
        elif line == '' and len(map_text_lines) > 0 :
            # Find the longest row in the map, set width to that value
            width = -1
            for line in map_text_lines :
                if width < len(line) :
                    width = len(line)

            # Set the height of the map to the map_text_lines length
            height = len(map_text_lines)

            # Add spaces to the end of shorter lines to ensure that the content is rectangular.
            for i in range(len(map_text_lines)) :
                map_text_lines[i] += ' ' * (width - len(map_text_lines[i]))

            # Convert map_text_lines to a level objects 
            for x in range(width) :
                map.append([])
            for y in range(len(map_text_lines)):
                for x in range(width) :
                    map[x].append(map_text_lines[y][x])

            # Find the starting location
            start_x = None
            start_y = None
            goal_x = None
            goal_y = None
            for x in range(width) :
                for y in range(height) :
                    current_square = map[x][y]
                    if current_square == '@' :
                        start_x = x
                        start_y = y
                    elif current_square == '.' :
                        goal_x = x
                        goal_y = y
            level = {'width': width,
                     'height': height,
                     'map': map,
                     'start': { 'x': start_x, 'y': start_y },
                     'goal':  { 'x': goal_x,  'y': goal_y  }
                    }
            levels.append(level)

            map_text_lines = []
            map = []
    return levels

if __name__ == '__main__':
    start()
