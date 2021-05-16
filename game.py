import pygame, sys, os

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (80,80,80)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)

RES_WID = 800
RES_HGT = 800
RESOLUTION = [RES_WID,RES_HGT]

pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
running = True

flower = pygame.image.load(os.path.join("flower.png"))
flower.convert()
skull = pygame.image.load(os.path.join("skull.png"))
skull.convert()

class Piece:
    def __init__(self, x, y, rad=40, color=BLACK, tp='flower'):
        self.x = x
        self.y = y
        self.rad = rad
        self.color = color
        self.tp = tp

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.rad)
        pygame.draw.circle(surface, WHITE, (self.x, self.y), self.rad-5, 2)
        if self.tp == 'flower':
            surface.blit(flower, (self.x-25, self.y-25))
        else:
            surface.blit(skull, (self.x-25, self.y-30))
            

pieces = [Piece((RES_WID/2)-90,RES_HGT-30, tp='skull'), 
    Piece((RES_WID/2)-30,RES_HGT-30), 
    Piece((RES_WID/2)+30,RES_HGT-30), 
    Piece((RES_WID/2)+90,RES_HGT-30)] 
while(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE)

    ## draw ##
    for piece in pieces:
        piece.draw(screen)
    pygame.draw.rect(screen, GRAY, pygame.Rect((RES_WID/2)-50, RES_HGT-200, 100, 100))
    pygame.display.flip()
pygame.quit()
