import libtcodpy as tcod
import numpy as np
from game_map import tiles, start, WIDTH, HEIGHT
from tile import Tile
import random
from threading import Thread
from time import sleep

# ######################################################################
# Global Game Settings
# ######################################################################
# Windows Controls
FULLSCREEN = False
SCREEN_WIDTH = 96  # characters wide
SCREEN_HEIGHT = 54  # characters tall
LIMIT_FPS = 60  # 20 frames-per-second maximum
# Game Controls
TURN_BASED = False  # turn-based game

map_pos = [start[0], start[1]]

chunk_size = 16

screen_values = []

chunk_ready = []

cooldown = 0.001

con = 0

# Based on the game_map values, this gets a np array with the tiles ONLY around the player
def GetScreenValues():
    global screen_values
    screen_values = np.empty((SCREEN_WIDTH, SCREEN_HEIGHT), dtype=Tile)

    i = 0
    j = 0
    for width in range(int(map_pos[0] - SCREEN_WIDTH/2), int(map_pos[0] + SCREEN_WIDTH/2)): # Loops through the values for what should be displayed on screen
        for height in range(int(map_pos[1] - SCREEN_HEIGHT/2), int(map_pos[1] + SCREEN_HEIGHT/2)): # loops through the height values for what should be displayed on screen
            if (width < 0 or height < 0 or width > WIDTH-1 or height > HEIGHT-1): # checks for stuff outside the map
                continue
            screen_values[i, j] = tiles[width][height]
            j+=1
        j=0
        i+=1

    print (screen_values)
    
# Draws the full map unless the tile to be drawn is already on screen
def DrawFullMap ():
    global screen_values

    # Checks to see if the p_screen has not been defined yet
    x = 0
    y = 0
    # Loops through the screen_values as well as the p_screen
    for i in range(screen_values.shape[0]):
        for j in range(screen_values.shape[1]):
            tile = GetTile(screen_values[i, j], i, j)
            set_char(tile, x, y)
            y+=1
        y=0
        x+=1

def DrawChunk (start_i, start_j):
    # while not tcod.console_is_window_closed() : 
        
        # if not AllChunksLoaded():

        # loops through all the tiles in screen_values and places them on screen
        for i in range(start_i, start_i + chunk_size):
            for j in range(start_j, start_j + chunk_size):
                if (i >= 96 or j >= 54):
                    continue
                if (i == player_x and j == player_y):
                    continue
                # (tile, color) = GetTile(screen_values[i, j], game_map.biomes[i, j], i, j)
                set_tile (screen_values[i, j].char, screen_values[i, j].color, i, j)

        # chunk_ready[chunk_i] = True

        # sleep(cooldown * 1.05)

        # else:
        #     for j in chunk_ready:
        #         chunk_ready[j] = False

# Checks to see if "all" chunks are loaded, meaning that if the majority of them are loaded, render them on screen
# def AllChunksLoaded():
#     i = 0
#     for chunk in chunk_ready:
#         if (chunk == True):
#             i += 1
#     print (i)
#     return i * 1.5 > len(chunk_ready)

def ThreadAllChunks ():
    while (1):
        # chunk_i = 0
        for i in range (0, int(SCREEN_WIDTH/chunk_size)+1):
            for j in range (0, int(SCREEN_HEIGHT/chunk_size)+1):
                # chunk_ready.append(False)
                renderer = Thread(target=DrawChunk, args=(i*chunk_size, j*chunk_size))
                renderer.start()
                # chunk_i += 1

def SetScreenValues():
    screen_values = GetScreenValues()


def set_color (color, x, y):
    if (tcod.console_get_char_foreground (0, x, y) == tcod.Color(color[0], color[1], color[2])):
        return
    else:
        tcod.console_set_char_foreground(0, x, y, color)

def set_char (c, x, y):
    if (con.ch[y, x] == ord(c)):
        return
    else:
        con.ch[y, x] = ord(c)

def set_tile (c, color, x, y):
    # print ((c, color))
    con.ch[y, x] = ord (c)
    con.fg[y, x] = tcod.Color(color[0], color[1], color[2])

def set_bg (color, x, y):
    con.bg[y, x] = tcod.Color(color[0], color[1], color[2])


# ######################################################################
# User Input
# ######################################################################
 
 
def keyHandler(key):
    # if key.vk == tcod.KEY_ENTER and key.lalt:
    #     # Alt+Enter: toggle fullscreen
    #     tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
 
     # movement keys
    if key == 119 : # W KEY
        map_pos[1] -= 1
 
    if key == 115 : # S KEY 
        map_pos[1] += 1
 
    if key == 97 : # A KEY
        map_pos[0] -= 1
 
    if key == 100 : # D KEY
        map_pos[0] += 1

    if (key == 119 or key == 115 or key == 97 or key == 100):
        # print (map_pos)
        print ('UWU!')
        GetScreenValues()
    
#############################################
# Main Game Loop
#############################################
 
 
def render_loop ():
    global player_x, player_y
    player_x = int (SCREEN_WIDTH / 2)
    player_y = int (SCREEN_HEIGHT / 2)

    ThreadAllChunks()

    # ValueLoop = Thread(target=GetScreenValues)
    # ValueLoop.start()

    # while not tcod.console_is_window_closed():
    #     sleep(cooldown * 1.1)
    #     con.ch [player_y, player_x] = ord ('@')
    #     con.fg [player_y, player_x] = tcod.white

def flusher_loop ():
    while not tcod.console_is_window_closed():
        con.ch [player_y, player_x] = ord ('@')
        con.fg [player_y, player_x] = tcod.white

        sleep(cooldown * 1.125)

        tcod.console_flush()

def main():
    # Setup player
 
    # Setup Font
    font_filename = 'arial16x16.png'
    tcod.console_set_custom_font(f"./assets/{font_filename}", tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
 
    # Initialize screen
    title = 'SkyMocha'
    global con
    con = tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, title, FULLSCREEN)
 
    # Set FPS
    tcod.sys_set_fps(LIMIT_FPS)
 
    SetScreenValues()
    # DrawFullMap(p_screen=-1)

    exit_game = False

    renderer = Thread(target=render_loop)
    renderer.start()

    flusher = Thread(target=flusher_loop)
    flusher.start()

    while not tcod.console_is_window_closed() and not exit_game:
    
        for event in tcod.event.get():
            if event.type == "KEYDOWN":
                exit_game = keyHandler(event.sym)
                sleep(cooldown * 0.95)

main()