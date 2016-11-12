# pyGameSkier.py
import pygame

# a world sprite is a pygame sprite
class worldSprite(pygame.sprite.Sprite):
    
    def __init__(self, location, picture):
        pygame.sprite.Sprite.__init__(self)
        self.image = picture
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def draw(self,screen):
        screen.blit(self.image, self.rect)
        # draw this sprite on the screen (BLIT)

# a skier in the world knows how fast it is going
# and it can move horizontally
class worldSkier(worldSprite):
    speed = 5
    def update(self, direction):
        self.rect.left += direction * self.speed
        self.rect.left = max(0, min(380, self.rect.left))

class skiWorld(object):
    running = False
    keydir = 0

    def __init__(self):
        self.running = True
        self.skier = worldSkier([190, 50], pygame.image.load("assets/skier.png"))

        ## adding trees
        self.trees = worldTreeGroup(pygame.image.load("assets/block.png"))

    def updateWorld(self):
        # the skier is part of the world and needs updating
        self.skier.update(self.keydir)

        ## move the tree rows - removing any
        ## line that is off the top of the screen
        self.trees.update()

        ## check if the skier has collided with any
        ## tree sprite in the tree rows in the tree group
        if pygame.sprite.spritecollide(self.skier, self.trees, False):
            self.running = False

        ## check if the tree group has run out of tree rows -
        ## skier got to the bottom of the piste
        if len(self.trees)==0:
            self.running = False

    def drawWorld(self, canvas):
        canvas.fill([255, 250, 250]) # make a snowy white background
        world.trees.draw(canvas) # draw the trees
        world.skier.draw(canvas) # draw the player on the screen

    def keyEvent(self, event):
        # event should be key event but we only move
        # if the key is pressed down and not released up
        self.keydir = (0 if event.type == pygame.KEYUP else -1 if event.key == pygame.K_LEFT else +1 if event.key == pygame.K_RIGHT else 0)

import random
class worldTreeGroup(pygame.sprite.Group):
    speed = 5
        
    def __init__(self, picture):
        pygame.sprite.Group.__init__(self)
        treePicture = picture
        treeRow = pygame.sprite.Group()
                
        # in rows with a gap somewhere in the middle
        # only have a line of trees every 5th row or the
        # game is too difficult
        for y in range(0, 400):
            if (y % 5 == 0): # every 5th, add tree row with a gap
                gapsize = 3 + random.randint(0,6) # size of gap
                # starting position of gap
                gapstart = random.randint(0,10 - (gapsize//2))
                        
                # create a row of 20 trees but 'gapsize'
                # skip trees in the middle
                for b in range(0,20):
                    if b >= gapstart and gapsize > 0:
                        gapsize-=1
                    else:
                        newtree=worldSprite([b*20, (y+10)*20],treePicture)
                        treeRow.add(newtree)
                                        
            self.add(treeRow)
                
    def update(self):
        for treeRow in self:
            treeRow.rect.top-=self.speed
            if treeRow.rect.top <= -20:
                treeRow.kill() # remove this block from ALL groups

import os
import platform
if platform.system() == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'windib'

# pygame library wants to do a few things before we can use it
pygame.init()
pygame.display.set_caption("pyGameSkier")
pygame.key.set_repeat(100, 5)

# create something to draw on with a size of 400 wide
canvas = pygame.display.set_mode([400, 500])

# we will need to have a constant time between frames
clock = pygame.time.Clock()

world = skiWorld()

# check input, change the game world and display the new game world
while (world.running):
    # check external events (key presses, for instance)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # stop running the game
            world.running = False
        elif (hasattr(event, 'key')): # process this keyboard input
            world.keyEvent(event)

    # update the game world
    world.updateWorld()

    # draw the world on the canvas
    world.drawWorld(canvas)

    # important to have a constant time between each display flip.
    # in this case, wait at least 1/30th second has passed
    clock.tick(30)

    # flip the display to show the newly drawn screen
    pygame.display.flip()

# once the game is not running, need to finish up neatly
pygame.quit()

