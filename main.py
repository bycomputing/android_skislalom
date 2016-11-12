try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
except ImportError:
    pass

import pygame, time, sys, os
from skiSlalom import worldSprite, worldSkier, skiWorld, worldTreeGroup
from textWrapping import *

class title(object):    
    def __init__(self, quit_callback, canvas, font, alpha = 1, color = [0,0,0]):
        self.quit_callback = quit_callback
        self.canvas = canvas
        self.font = font
        self.alpha = alpha
        self.color = color       
         
    def center(self, across=False, down=False):
        self.centered_across = across
        self.centered_down = down

    def display(self, message, wait = 2, pos = (0,0)):
        text_image = self.font.render(message, self.alpha, self.color)
        if self.centered_across:
            pos = ((self.canvas.get_width() - text_image.get_width()) / 2, pos[1])
        if self.centered_down:
            pos = (pos[0], (self.canvas.get_height() - text_image.get_height()) / 2)
        self.canvas.blit(text_image, pos)
        for event in pygame.event.get():            
            self.quit_callback(event)
        pygame.display.update()
        time.sleep(wait)

def check_android_events(event):
    # stop running the game
    if event.type == pygame.QUIT or \
       event.type == pygame.KEYDOWN and event.key == pygame.K_AC_BACK or \
       event.type == pygame.APP_WILLENTERBACKGROUND or \
       event.type == pygame.APP_DIDENTERFOREGROUND:
        pygame.quit()
        sys.exit()          

# pygame library wants to do a few things before we can use it
pygame.init()
pygame.display.set_caption("pyGameSkier")
pygame.key.set_repeat(100, 5)
pygame.font.init()

# constants
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
SNOWY_WHITE = (255, 250, 250)

# vars
running = True
instruction = 'See if you can get him to the bottom of the slope. Slide to control player.'
font = pygame.font.Font('assets/DejaVuSans.ttf', 28)
canvas = pygame.display.set_mode([400, 500]) # create something to draw on with a size of 400 wide
canvas.fill(SNOWY_WHITE)
world = skiWorld(canvas)

game_title = title(check_android_events, canvas, font, color = RED)
game_title.center(True, True)
game_title.display('Ski Slalom ver. 1.1')
texts = wrapline(instruction, font, canvas.get_width())
canvas.fill(SNOWY_WHITE)
for text in texts:
    game_title.display(text)
    canvas.fill(SNOWY_WHITE)
game_title.display('Ready!')

music = pygame.mixer.Sound("assets/tune.ogg")
music.play(-1)

# we will need to have a constant time between frames
clock = pygame.time.Clock()

# check input, change the game world and display the new game world
while True:
    while (world.running):
        # check external events (key presses, for instance)        
        for event in pygame.event.get():
            check_android_events(event)                
            if (hasattr(event, 'key')): # process this keyboard input
                world.keyEvent(event)
            elif (hasattr(event, 'pos')):
                world.mouseEvent(event)

        # important to have a constant time between each display flip.
        # in this case, wait at least 1/30th second has passed
        dt = clock.tick(30)

        # update the game world
        world.updateWorld(dt / 1000.0)

        # draw the world on the canvas
        world.drawWorld()

        # flip the display to show the newly drawn screen
        pygame.display.flip()       
    music.stop()
    if len(world.trees) != 0:
        game_title.display('You got caught!')
        canvas.fill(SNOWY_WHITE)
        game_title.display('Try again.')
        canvas.fill(SNOWY_WHITE)
        game_title.display('Ready!')
        world = skiWorld(canvas)
        music.play(-1)
        clock = pygame.time.Clock()
    else:
        game_title.display('Congratulations!')
        canvas.fill(SNOWY_WHITE)
        game_title.display('You made it!')        
        break
# once the game is not running, need to finish up neatly
pygame.quit()
sys.exit()
