import pygame
from build import Create
from movement import Player
import math
import time

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong 1.2")
meniu = True
ok = True
won = False
creator = Create()

# Set up the clock for framerate control
clock = pygame.time.Clock()
FPS = 100

cube_length = 30
level = 9
numOfCubes = 0

frame_counter = 0
frame = 1

# coord of play button
button_x = 450
button_y = 270
button_width = 300
button_height = 74

# for platform
whidth = 200
hight = 30
coord_x, coord_y = 500, 600
platform = ''

# for ball
radius = 6
ball_x = coord_x + 50
ball_y = coord_y - radius
ball = ''
angle = math.radians(240)
old = angle
new =  True

enter_level = False
score = [[None for _ in range(9)] for _ in range(4)]
levels = [[False for _ in range(9)] for _ in range(4)] # array for levels
button = [[None for _ in range(9)] for _ in range(4)]

level_page = False # if it is on the level page

# read from the setup file
path = './docs/setup' # make reset button for setup
# read for scores
with open(path, "r") as file:
    elem = file.read()

cnt = 0
elem = elem.split()
for i in range(1, 4):
    for j in range(1, 9):
        score[i][j] = int(elem[cnt])
        cnt += 1
        levels[i][j] = eval(elem[cnt])
        cnt += 1

# read for levels
levels[1][1] = True
# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Check for mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # play button pressed
            if meniu and button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                #enter_level = True
                level_page = True # move to level page
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            elif meniu and button_x < mouse_x < button_x + button_width and button_y + 318 < mouse_y < button_y + button_height + 318:
                running = False
            elif level_page and 30 < mouse_x < 30 + 70 and 30 < mouse_y < 30 + 70:
                level_page = False
            elif level_page:
                for i in range(1, 4):
                    for j in range(1, 9):
                        # enter the level
                        if levels[i][j] and button[i][j].x < mouse_x < button[i][j].x + 130 and button[i][j].y < mouse_y < button[i][j].y + 130:
                            level = (i - 1) * 8 + j

                            # check if the level is avalable
                            if levels[i][j] == True:
                                level_page = False
                                meniu = False
                                enter_level = True
                                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            elif meniu and not level_page and button_x < mouse_x < button_x + button_width and button_y + 210 < mouse_y < button_y + button_height + 210: # reset the game
                # reset the progress
                for i in range(1, 4):
                    for j in range(1, 9):
                        levels[i][j] = False
                levels[1][1] = True


    frame_counter += 1

    # make the meniu
    if meniu == True: 
        
        if level_page == False:
            # create the background
            Create.showImage(screen, creator.meniu_image, 0, 0)
            

            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button_x < mouse_x < button_x + button_width and (button_y < mouse_y < button_y + button_height or button_y + 318 < mouse_y < button_y + button_height + 318 or button_y + 210 < mouse_y < button_y + button_height + 210):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else: # if on the level page

            # create the background 
            Create.showImage(screen, creator.levels_image, 0, 0)

            # draw the lelev buttons
            if ok == True:
                ok = False
                for i in range(1, 4):
                    for j in range(1, 9):
                        button[i][j] = pygame.draw.rect(screen, 'RED', (50 + (j - 1) * 140, 160 + (i - 1) * 178, 130, 130))
            
            # draw the level locks
            for i in range(1, 4):
                for j in range(1, 9):
                    if levels[i][j] == False:
                        Create.showImage(screen, creator.lock_image, button[i][j].x + 20, button[i][j].y + 20)

            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 30 < mouse_x < 30 + 70 and 30 < mouse_y < 30 + 70:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
            for i in range(1, 4):
                for j in range(1, 9):
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if levels[i][j] and button[i][j].x < mouse_x < button[i][j].x + 130 and button[i][j].y < mouse_y < button[i][j].y + 130:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
            
    else: # when in game
        # create the background every frame
        Create.showImage(screen, creator.background_image, 0, 0)

        # make the platform every frame
        platform = Create.showImage(screen, creator.platform_image, coord_x, coord_y)

        # draw the ball every frame
        ball = pygame.draw.circle(screen, 'WHITE', (ball_x, ball_y), radius)


        # read the file once
        if enter_level == True:
            handles = Create.makeMat(level, creator.block_image, screen)
            enter_level = False
            handles = Create.makeLvl(screen, creator.block_image, handles)

            # make the initial trajectory line
            stop_x, stop_y = Player.calcCoords(ball_x, ball_y, angle)

            line = pygame.draw.line(screen, 'WHITE', (ball_x, ball_y), (stop_x, stop_y))
            index, punct = Player.findCube(ball_x, ball_y, handles, (ball_x, ball_y), (stop_x, stop_y), screen)
            dimVechi = len(handles)
        else:
            # build the cubes
            handles = Create.makeLvl(screen, creator.block_image, handles)

        # check if the angle has changed
        if old != angle:
            # calculate the stop coords
            stop_x, stop_y = Player.calcCoords(ball_x, ball_y, angle)
            old = angle

            # draw the line
            index, punct = Player.findCube(ball_x, ball_y, handles, (ball_x, ball_y), (stop_x, stop_y), screen)
            dimVechi = len(handles)


        if dimVechi != len(handles):
            index, punct = Player.findCube(ball_x, ball_y, handles, (ball_x, ball_y), (stop_x, stop_y), screen)
            dimVechi = len(handles)
        
        # check if to move the ball
        if frame_counter >= frame:
            # move the ball
            frame_counter = 0
            ball_x, ball_y, angle, handles, status = Player.ballMv(ball_x, ball_y, angle, handles, platform, index, punct, (ball_x, ball_y), (stop_x, stop_y))

        # check the status
        if status == "WIN": # display some message
            level += 1
            levels[(level - 1) // 8 + 1][(level - 1) % 8 + 1] = True
            won = True

        elif status == "LOSS": # display some message
            won = True

    rasp, coord_x, coord_y = Player.pressedKey(meniu, level_page, coord_x, coord_y)
    # decision to exist while in menu
    if rasp == 'EXIT':
        running = False
    elif rasp == 'MENIU' or won == True:
        # reset the coord
        coord_x, coord_y = 500, 600 
        # ball coord for start
        ball_x = coord_x + 50
        ball_y = coord_y - radius
        angle = math.radians(240) # reset the angle
        level_page = False
        if won == True:
            level_page = True
        
        won = False
        old = angle
        new = True
        enter_level = True
        meniu = True
    elif rasp == 'LEVEL':# move to the level room
        level_page = False
        time.sleep(0.2)
    
    # Update the display
    pygame.display.update()

    clock.tick(FPS)

# Clean up and quit Pygame
pygame.quit()

# write into the setup file
with open(path, 'w') as file:

    for i in range(1, 4):
        for j in range(1, 9):
            file.write(str(score[i][j]) + ' ')
            file.write(str(levels[i][j]) + ' ')
            