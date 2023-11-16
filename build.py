import pygame

meniu_path = './docs/pics/meniu.png'
block_path = './docs/pics/block.png'
platform_path = './docs/pics/platform.png'
background_path = './docs/pics/background.png'
playbutton_path = './docs/pics/playbutton.png'
levels_path = './docs/pics/levels.png'
lock_path = './docs/pics/lock.png'

meniu_image = ''
block_image = ''
platform_image = ''
background_image = ''
playbutton_image = ''
levels_image = ''
lock_image = ''

HEIGHT = 800
WEIGHT = 1200

class Create:

    # Constructor
    def __init__(self):
        # Loading the images
        self.meniu_image = pygame.image.load(meniu_path)
        self.block_image = pygame.image.load(block_path)
        self.platform_image = pygame.image.load(platform_path)
        self.background_image = pygame.image.load(background_path)
        self.playbutton_image = pygame.image.load(playbutton_path)
        self.levels_image = pygame.image.load(levels_path)
        self.lock_image = pygame.image.load(lock_path).convert_alpha()


        # Scaling the images
        self.meniu_image = pygame.transform.scale(self.meniu_image, (WEIGHT, HEIGHT))
        self.block_image = pygame.transform.scale(self.block_image, (30, 30))
        self.platform_image = pygame.transform.scale(self.platform_image, (200, 30))
        self.background_image = pygame.transform.scale(self.background_image, (WEIGHT, HEIGHT))
        self.playbutton_image = pygame.transform.scale(self.playbutton_image, (74, 300))
        self.levels_image = pygame.transform.scale(self.levels_image, (WEIGHT, HEIGHT))
        self.lock_image = pygame.transform.scale(self.lock_image, (80, 80))

    # Method to show an image
    def showImage(screen, image, coord_x, coord_y):
        return screen.blit(image, (coord_x, coord_y))
    
    # read the matrix with the level info
    def makeMat(level, image, screen):

        # read the file
        with open("./docs/level" + str(level) + "/matrix", "r") as file:
            content = file.read()
        
        # split numbers
        content = content.split()

        number_of_blocks = int(content[0])
        
        content[0] = int(content[0])
        # get every coords
        for i in range(1, 2 * number_of_blocks - 2, 1):
            content[i] = int(content[i])

        handle = [None] * (content[0] + 1)

        for i in range(1, content[0] + 1):

            handle[i] = screen.blit(image, (int(content[2 * i]), int(content[2 * i - 1])))

        return handle
    
    def makeLvl(screen, image, handle):
        
        dim = len(handle)
        # make every cube
        for i in range(1, dim):
            handle[i] = screen.blit(image, (handle[i].x, handle[i].y))
        
        return handle
