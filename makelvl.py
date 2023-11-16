import pygame
import time

nume = './docs/level'
block_path = './docs/pics/block.png'


rows = 540 // 30

columns = 1200 // 30

# get the level from console
level = input("Enter the level number: ")

# make the file path
nume = nume + str(level) + '/matrix'

# open the window
WIDTH , HEIGHT = 1200, 540


# Initialize Pygame
pygame.init()

timer = pygame.time.get_ticks()  # Initialize timer

# Create a display surface (window)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the title of the window
pygame.display.set_caption("Make Level" + ' ' + str(level))

block_image = pygame.image.load(block_path)
block_image = pygame.transform.scale(block_image, (30, 30))

matrix = [[False] * columns for _ in range(rows)]
button_rect = [[None] * columns for _ in range(rows)]

# read from file the current format file


# Open the file for reading
with open(nume, "r") as file:
    content = file.readline().strip()  # Read the first line and remove leading/trailing spaces

# Split the content into individual elements
elements = content.split()

for i in range(1, int(elements[0]) + 1):
    matrix[int(elements[2 * i - 1]) // 30][int(elements[2 * i]) // 30] = True



for i in range(rows):
    for j in range(columns):
        # Button properties
        button_rect[i][j] = block_image.get_rect(topleft=(j * 30, i * 30))

last = (0, 0, 0, 0)
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            

    # Clear the screen
    screen.fill((0, 0, 0))
    
    for i in range(rows):
        for j in range(columns):
            x, y = pygame.mouse.get_pos()

            if button_rect[i][j].x < x < button_rect[i][j].x + 30 and button_rect[i][j].y < y < button_rect[i][j].y + 30:
                #pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                mouse_buttons = pygame.mouse.get_pressed()
                current_time = pygame.time.get_ticks()
                if mouse_buttons[0] and button_rect[i][j].collidepoint((x, y)) and (last != button_rect[i][j] or current_time - timer > 500):  # 0 index corresponds to the left mouse button
                    last = button_rect[i][j]
                    timer = current_time
                    if matrix[i][j]:
                        matrix[i][j] = False
                    else:
                        matrix[i][j] = True

    # Draw the buttons that are clicked
    for i in range(rows):
        for j in range(columns):
            if matrix[i][j]:
                screen.blit(block_image, button_rect[i][j])

    x, y = pygame.mouse.get_pos()
    for i in range(rows):
        for j in range(columns):
            if button_rect[i][j].x < x < button_rect[i][j].x + 30 and button_rect[i][j].y < y < button_rect[i][j].y + 30:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    elif keys[pygame.K_c]:
        # clear the canvas
        for i in range(rows):
            for j in range(columns):
                matrix[i][j] = False
    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()

# write in the file the cubes' positions
cnt = 0
for i in range(rows):
    for j in range(columns):
        if matrix[i][j]:
            cnt += 1
with open(nume, "w") as file:
    file.write(str(cnt) + ' ')

    for i in range(rows):
        for j in range(columns):
            if matrix[i][j]:
                file.write(str(button_rect[i][j].y) + ' ' + str(button_rect[i][j].x) + ' ')