import os, sys
import pygame
from pygame.locals import *

pygame.init()

#Set the window
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
SURFACE = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

#Set the window title
pygame.display.set_caption('Deeper')

#We need a set FPS for animations
FPS = 30
FPS_CLOCK = pygame.time.Clock()

#Some Constants to Use
TILE_HEIGHT = 64
TILE_WIDTH = 64
BGCOLOR = (255,0,255)

# Directions
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
NODIR = 4

# Fonts 
def font(size = 18) : return pygame.font.Font('Liberator.ttf', size)
DEFAULT_FONT = font()

def start() :
    global LEVELS, LEVEL_INDEX, SPRITES, LEVEL_MAP, PLAYER_DATA
    LEVELS = parse_level_file('levels.txt')
    LEVEL_INDEX = 0
    #Sprite Map
    SPRITES = {'wall':pygame.image.load('Images/wall.png'),
            'player':pygame.image.load('Images/player.png'),
            'floor':pygame.image.load('Images/floor.png')}
    #Floor Map
    LEVEL_MAP = {'#':SPRITES['wall'],
            ' ':SPRITES['floor']}

    #Player Data
    PLAYER_DATA = {'x':LEVELS[LEVEL_INDEX]['start']['x'],
                'y':LEVELS[LEVEL_INDEX]['start']['y'],
                'pixelX': LEVELS[LEVEL_INDEX]['start']['x']*TILE_WIDTH,
                'pixelY': LEVELS[LEVEL_INDEX]['start']['x']*TILE_HEIGHT}

    startscreen()
    
    while True:
        result = play_level()

        if result == 'caught' :
            pass
        elif result == 'succeeded' :
            pass


def play_level() :
    global CURRENT_IMAGE
    CURRENT_LEVEL = LEVELS[ LEVEL_INDEX ]
    direction = NODIR
    # MAP = # ...
    # Handle all events here
    pygame.key.set_repeat(5,5)
    while True:
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
            move_player(direction)
        SURFACE.fill(BGCOLOR)
        mapSurface = draw_map(CURRENT_LEVEL)
        mapSurfaceRect = mapSurface.get_rect()
        mapSurfaceRect.center = (320, 240)
        SURFACE.blit(mapSurface,mapSurfaceRect)
        #update the display
        pygame.display.update()
        #Wait a tick to draw the next frame
        FPS_CLOCK.tick(FPS)

def move_player(direction):
    x = PLAYER_DATA['pixelX']
    y = PLAYER_DATA['pixelY']
    if (direction == DOWN):
        if not isWall(int(x/TILE_WIDTH), int(y/TILE_HEIGHT)+1):
            PLAYER_DATA['pixelY'] += 1
    elif (direction == RIGHT):
        if not isWall(int(x/TILE_WIDTH)+1,int(y/TILE_HEIGHT)):
            PLAYER_DATA['pixelX'] += 1
    elif (direction == UP):
        if not isWall(int(x/TILE_WIDTH),int(y/TILE_HEIGHT)):
            PLAYER_DATA['pixelY'] -= 1
    elif (direction == LEFT):
        if not isWall(int(x/TILE_WIDTH)-1,int(y/TILE_HEIGHT)):
            PLAYER_DATA['pixelY'] -= 1

def isWall(x, y):
    print '======='
    print x
    print y
    print '========'
    return (LEVELS[LEVEL_INDEX]['map'][x][y] == '#')

def draw_map(level):
    mapDrawWidth = int(level['width']*TILE_WIDTH)
    mapDrawHeight = int(level['height']*TILE_HEIGHT)
    mapDrawSurface = pygame.Surface((mapDrawWidth, mapDrawHeight))
    mapDrawSurface.fill(BGCOLOR)
    for x in range(level['width']):
        for y in range(level['height']):
            tile = pygame.Rect((x*TILE_WIDTH),(y*TILE_HEIGHT), TILE_WIDTH, TILE_HEIGHT)
            if level['map'][x][y] in LEVEL_MAP:
                tileImg = LEVEL_MAP[level['map'][x][y]]
            else:
                tileImg = LEVEL_MAP[' ']
            mapDrawSurface.blit(tileImg, tile)
    playerImg = SPRITES['player']
    #playerTile = pygame.Rect(PLAYER_DATA['x']*TILE_WIDTH, PLAYER_DATA['y']*TILE_HEIGHT,TILE_WIDTH, TILE_HEIGHT)
    playerTile = pygame.Rect(PLAYER_DATA['pixelX'],PLAYER_DATA['pixelY'],TILE_WIDTH,TILE_HEIGHT)
    mapDrawSurface.blit(playerImg, playerTile)
    return mapDrawSurface   

def startscreen() :
    title = "Sneaky Spy Man Bro Child Son"

    display_text(title, {'alignment' : 'center'}, font(40) )

    while True :
        for event in pygame.event.get() :
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN :
                return

        pygame.display.update()
        FPS_CLOCK.tick()


def display_text(text, spec, font = DEFAULT_FONT) :
    rendered_text = font.render(text, 1, (252,231,206))
    rect = rendered_text.get_rect()

    width = rect.width
    height = rect.height

    if 'x' in spec : rect.x = spec['x']
    if 'y' in spec : rect.y = spec['y']

    if 'alignment' in spec :
        a = spec['alignment']
        if a == 'center' :
            rect.x = ( WINDOW_WIDTH - width ) // 2
        elif a == 'left' :
            rect.x = 0
        elif a == 'right' :
            rect.x = WINDOW_WIDTH - width

    if 'v_alignment' in spec :
        a = spec['v_alignment']
        if a == 'center' :
            rect.y = ( WINDOW_HEIGHT - height ) // 2
        elif a == 'top' :
            rect.y = 0
        elif a == 'bottom' :
            rect.y = WINDOW_HEIGHT - height

    SURFACE.blit(rendered_text, rect)

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
