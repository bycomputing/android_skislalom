try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
except ImportError:
    pass

import pygame, random

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
    speed = 150
    def update(self, direction, dt):
        self.rect.left += direction * self.speed * dt
        self.rect.left = max(0, min(380, self.rect.left))

class skiWorld(object):
    running = False
    keydir = 0

    def __init__(self, canvas):        
        self.running = True
        self.canvas = canvas
        self.canvas_w, self.canvas_h = self.canvas.get_size()        
        self.skier = worldSkier([190, 50], pygame.image.load("assets/skier.png"))

        ## adding trees
        self.trees = worldTreeGroup(pygame.image.load("assets/block.png"), self.canvas_w)

    def updateWorld(self, dt):
        # the skier is part of the world and needs updating
        self.skier.update(self.keydir, dt)

        ## move the tree rows - removing any
        ## line that is off the top of the screen
        self.trees.update(dt)

        ## check if the skier has collided with any
        ## tree sprite in the tree rows in the tree group
        if pygame.sprite.spritecollide(self.skier, self.trees, False):
            self.running = False

        ## check if the tree group has run out of tree rows -
        ## skier got to the bottom of the piste
        if len(self.trees)==0:
            self.running = False

    def drawWorld(self):
        self.canvas.fill([255, 250, 250]) # make a snowy white background
        self.trees.draw(self.canvas) # draw the trees
        self.skier.draw(self.canvas) # draw the player on the screen

    def keyEvent(self, event):
        # event should be key event but we only move
        # if the key is pressed down and not released up
        self.keydir = (0 if event.type == pygame.KEYUP \
                       else -1 if event.key == pygame.K_LEFT \
                       else +1 if event.key == pygame.K_RIGHT else 0)

    def mouseEvent(self, event):
        self.skier.rect.left = event.pos[0]
        
class worldTreeGroup(pygame.sprite.Group):
    speed = 150
        
    def __init__(self, picture, canvas_w):
        pygame.sprite.Group.__init__(self)
        treePicture = picture
        treeRow = pygame.sprite.Group()
                
        # in rows with a gap somewhere in the middle
        # only have a line of trees every 5th row or the
        # game is too difficult
        for y in range(0, canvas_w):
            if (y % 5 == 0): # every 5th, add tree row with a gap
                gapsize = 3 + random.randint(0,6) # size of gap
                # starting position of gap
                gapstart = random.randint(0,10 - (gapsize//2))
                        
                # create a row of 20 trees but 'gapsize'
                # skip trees in the middle
                for b in range(0, 20):
                    if b >= gapstart and gapsize > 0:
                        gapsize-=1
                    else:
                        newtree=worldSprite([b*(canvas_w/20), (y+10)*20], treePicture)
                        treeRow.add(newtree)
                                        
            self.add(treeRow)
                
    def update(self, dt):
        for treeRow in self:
            treeRow.rect.top-=self.speed * dt
            if treeRow.rect.top <= -20:
                treeRow.kill() # remove this block from ALL groups
