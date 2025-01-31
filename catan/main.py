import pygame

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH*0.8)

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Catan')

clock = pygame.time.Clock()
FPS = 60
BG = (255, 255, 255)
run = True
from math import pi, cos, sin
def draw_bg():
    screen.fill(BG)

def draw_ntagon(surf, n, position, radius, colour):
    x, y = position
    angle = 2*pi/n
    points = []
    for i in range(n):
        xp = x + cos(angle*i)*radius
        yp = y + sin(angle*i)*radius
        points.append((xp, yp))
    return pygame.draw.polygon(surf, colour, points)
    

while run:
    clock.tick(FPS)
    draw_bg()
    draw_ntagon(screen, 3, (200, 250), 30, (0, 255, 0))
    ret = draw_ntagon(screen, 6, (400, 500), 50, (0, 255, 0))
    ret.collidepoint((0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

                
    pygame.display.update()
pygame.quit()