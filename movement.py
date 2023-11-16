import pygame
import time
import math

WIDTH, HEIGHT = 1200, 800

speed = 4

platform_length = 100

class Player:
    def __init__(self) -> None:
        pass
    
    def pressedKey(meniu, level_page, coord_x, coord_y):

        keys = pygame.key.get_pressed()
        # if the game is in meniu
        if meniu == True:
            # exit the game
            if level_page == False and keys[pygame.K_ESCAPE]:
                return 'EXIT', coord_x, coord_y
            elif level_page == True and keys[pygame.K_ESCAPE]:
                return 'LEVEL', coord_x, coord_y # move to the menu page
            
        # if the game isn t in meniu
        else:
            move = 5
            # for right
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                coord_x += move
                if coord_x + platform_length > WIDTH:
                    coord_x = WIDTH - platform_length
                
                return '', coord_x, coord_y
            # for left
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                coord_x -= move
                if coord_x < 0:
                    coord_x = 0
                
                return '', coord_x, coord_y
            # go to menu
            if keys[pygame.K_ESCAPE]:
                time.sleep(0.2)
                return 'MENIU', coord_x, coord_y
        return '', coord_x, coord_y

    # move the ball until it is a colision
    def ballMv(ball_x, ball_y, angle, handle, platform, index, punct, start, end):
        
        movement_speed = speed
        found = False
        status = ''

        # check colision of traj with blocks
        if index != 0 and (handle[index].x - 6 <= ball_x <= handle[index].x + 30 + 6) and (handle[index].y - 6 <= ball_y <= handle[index].y + 30 + 6):
            found = True
            
            x, y = punct
            if x % 30 == 29:
                x += 1
            if y % 30 == 29:
                y += 1
            
            # check if on edge
            if (y == handle[index].y + 30 and x == handle[index].x + 30) or (y == handle[index].y and x == handle[index].x) or (y == handle[index].y and x == handle[index].x + 30) or (y == handle[index].y + 30 and x == handle[index].x):
                angle = angle + math.radians(180)
            # if the bottom line
            elif y == handle[index].y + 30:
                #angle = math.radians(180) - angle
                angle = -angle
            elif y == handle[index].y: # the first line
                #angle = math.radians(180) - angle
                angle = -angle
            elif x == handle[index].x + 30:
                angle = math.radians(180) - angle
                #angle = -angle
            elif x == handle[index].x:
                #angle = -angle
                angle = math.radians(180) - angle
            
            handle.pop(index)
            
        # verify if won
        if len(handle) == 1:
            status = "WIN"

        rasp = platform.clipline(start, end)
        # colision with platform
        if found == False and rasp:

            if platform.x - 3 <= ball_x <= platform.x + 200 + 3 and platform.y - 3 <= ball_y <= platform.y + 30 + 3:# to add 6
                aux, aux1 = rasp
                x1, y1 = aux
                x2, y2 = aux1
                if int((ball_x - x1) ** 2 + (ball_y - y1) ** 2) < int((ball_x - x2) ** 2 + (ball_y - y2) ** 2):
                    x = x1
                    y = y1
                else:
                    x = x2
                    y = y2
                if y % 600 == 599:
                    y += 1

                # add collision check if in bounderies
                if x == int(ball_x) and y == int(ball_y):
                    # calculate the angle based on the point
                    dist = platform.x + 50 - x
                    grd = 270 - 78 * (dist / 100) 
                    # if the platform is moving
                    angle = math.radians(grd)

        # colision with borders
        dx = movement_speed * math.cos(angle)
        dy = movement_speed * math.sin(angle)

        if ball_x + dx <= 0 or ball_x + dx >= 1200:
            angle = math.radians(180) - angle
            if ball_x + dx <= 0:
                ball_x = 0
            if ball_x + dx >= 1200:
                ball_x = 1200
            dx = 0
            dy = 0
        elif ball_y + dy <= 0 or ball_y + dy >= 650:
            angle = - angle
            if ball_y + dy <= 0:
                ball_y = 0
            # case of loosing the game
            if ball_y + dy >= 650:
                status = "LOSS"
                ball_y = 650
            dx = 0
            dy = 0
        
        return ball_x + dx, ball_y + dy, angle, handle, status
    
        
    def calcCoords(x, y, angle):
        movement = speed
        dx = movement * math.cos(angle)
        dy = movement * math.sin(angle)

        while 0 <= x and x <= 1200 and 0 <= y and y <= 650:
            y += dy
            x += dx
        
        x -= dx
        y -= dy
        return x, y

    # return index of the closest cube on the trajectory
    def findCube(ball_x, ball_y, handle, start, end, screen):
        dim = len(handle)

        minim = 1000000
        index = 0
        cnt = 0
        primul = (-1, -1)
        for i in range(1, dim):

            # check for colision
            rasp = handle[i].clipline(start, end)
            if rasp:
                cnt += 1
                calc = int(math.sqrt((ball_x - handle[i].x) ** 2 + (ball_y - handle[i].y) ** 2))
                punct, aux = rasp
                if calc < minim:
                    minim = calc
                    index = i
                    x1, y1 = punct
                    x2, y2 = aux
                    # find the closest point to the ball
                    if int((ball_x - x1) ** 2 + (ball_y - y1) ** 2) < int((ball_x - x2) ** 2 + (ball_y - y2) ** 2):
                        primul = punct
                    else:
                        primul = aux

        return index, primul