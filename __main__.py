import os, sys
import pygame
from pygame.locals import *
from classes import *

pygame.init()

#Set the window
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
HALF_WINDOW_WIDTH = WINDOW_WIDTH // 2
HALF_WINDOW_HEIGHT = WINDOW_HEIGHT // 2

SURFACE = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

#Set the window title
pygame.display.set_caption('Deeper')

#We need a set FPS for animations
FPS = 30
FPS_CLOCK = pygame.time.Clock()

VELOCITY = 4

#Some Constants to Use
TILE_WIDTH = 64
BGCOLOR = (255,0,255)

# Directions
UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3
NODIR = 4

# Fonts 
def font(size = 18) : return pygame.font.Font('Liberator.ttf', size)
DEFAULT_FONT = font()

def start() :
    global LEVELS, LEVEL_INDEX, SPRITES, LEVEL_MAP, PLAYER
    LEVELS = parse_level_file('levels.txt')
    LEVEL_INDEX = 0

    # Sprite dictionary
    SPRITES = {
                'wall':   pygame.image.load('Images/wall.png'),
                'player': pygame.image.load('Images/player.png'),
                'floor':  pygame.image.load('Images/floor.png')
              }

    # Level Map to Sprite conversion dictionary
    LEVEL_MAP = {
                 '#': SPRITES['wall'],
                 ' ': SPRITES['floor']
                }

    CURRENT_LEVEL = LEVELS[ LEVEL_INDEX ]

    sprite_width = 16
    half_sprite_width = sprite_width // 2

    player_rect = pygame.Rect(HALF_WINDOW_WIDTH  - half_sprite_width,
                              HALF_WINDOW_HEIGHT - half_sprite_width,
                              sprite_width, sprite_width)

    PLAYER = Player(SPRITES['player'], player_rect)
    startscreen()
    
    while True:
        result = play_level()

        if result == 'caught' :
            pass
        elif result == 'succeeded' :
            pass


def play_level() :
    global CURRENT_LEVEL
    CURRENT_LEVEL = LEVELS[ LEVEL_INDEX ]

    start = CURRENT_LEVEL.start
    PLAYER.x = (CURRENT_LEVEL.width - start.x) * 64 - 20
    PLAYER.y = (CURRENT_LEVEL.height - start.y) * 64 - 20

    pygame.key.set_repeat(5,5)
    while True:
        # All event handlers
        for event in pygame.event.get():
            if event.type == QUIT: terminate()
            elif event.type == KEYDOWN:
                if event.key >= K_UP and event.key <= K_LEFT:
                    direction = event.key - K_UP
                elif event.key == K_w: direction = UP
                elif event.key == K_s: direction = DOWN
                elif event.key == K_d: direction = RIGHT
                elif event.key == K_a: direction = LEFT
                elif (event.key == K_ESCAPE): terminate()
                else : direction = NODIR
                move_player(direction)

        # Draw the background
        SURFACE.fill(BGCOLOR)

        #===========================================#
        # Generate the map content relative to the viewport/player location
        map_surface = draw_map()
        map_surface_rect = map_surface.get_rect()
        map_surface_rect.center = (PLAYER.x - 135, PLAYER.y + 42) # NOTE: These transformations only work for the current window resolution

        # Draw the map
        SURFACE.blit(map_surface, map_surface_rect)
        #===========================================#
        # Draw the player
        SURFACE.blit( PLAYER.sprite, PLAYER.rect )
        # Draw the frame
        pygame.display.update()
        # Wait for the frame to tick before proceeding to render the next frame
        FPS_CLOCK.tick(FPS)

def move_player(direction):
    x, y = PLAYER.x, PLAYER.y

    if   direction == UP:    y += VELOCITY
    elif direction == DOWN:  y -= VELOCITY
    elif direction == RIGHT: x -= VELOCITY
    elif direction == LEFT:  x += VELOCITY

    if not_in_wall(x, y):
        PLAYER.x, PLAYER.y = x, y
    elif not_in_wall(x, PLAYER.y):
        print("y")
        PLAYER.y //= TILE_WIDTH
        PLAYER.y += 1
        PLAYER.y *= TILE_WIDTH
        PLAYER.y -= 8
    else:
        print("x")
        PLAYER.x //= TILE_WIDTH
        PLAYER.x += 1
        PLAYER.x *= TILE_WIDTH
        PLAYER.x -= 8

def not_in_wall(x, y):
    x //= TILE_WIDTH
    y //= TILE_WIDTH

    width = CURRENT_LEVEL.width
    height = CURRENT_LEVEL.height

    return( x >= 0 and x < width and 
            y >= 0 and y < height and
            CURRENT_LEVEL.map[width - x - 1][height - y - 1] in (' ', '@'))

def draw_map():
    mapDrawWidth = CURRENT_LEVEL.width * TILE_WIDTH
    mapDrawHeight = CURRENT_LEVEL.height * TILE_WIDTH
    mapDrawSurface = pygame.Surface((mapDrawWidth, mapDrawHeight))
    mapDrawSurface.fill(BGCOLOR)
    map = CURRENT_LEVEL.map
    for x in range(CURRENT_LEVEL.width):
        for y in range(CURRENT_LEVEL.height):
            tile = pygame.Rect((x*TILE_WIDTH),(y*TILE_WIDTH), TILE_WIDTH, TILE_WIDTH)
            if map[x][y] in LEVEL_MAP:
                tileImg = LEVEL_MAP[map[x][y]]
            else:
                tileImg = LEVEL_MAP[' ']
            mapDrawSurface.blit(tileImg, tile)
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
            start = goal = None
            for x in range(width) :
                for y in range(height) :
                    current_square = map[x][y]
                    if current_square == '@' :
                        start = Point(x, y)
                    elif current_square == '.' :
                        goal = Point(x, y)
            print start.x
            print start.y
            level = Level(map, start, goal)
            # level = {'width': width,
            #          'height': height,
            #          'map': map,
            #          'start': { 'x': start_x, 'y': start_y },
            #          'goal':  { 'x': goal_x,  'y': goal_y  }
            #         }
            levels.append(level)

            map_text_lines = []
            map = []
    return levels

def terminate() :
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    start()
