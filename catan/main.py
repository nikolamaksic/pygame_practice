import pygame
from utils.Tile import Tile

pygame.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = int(SCREEN_WIDTH*0.8)

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Catan')

GAME_FONT = pygame.font.SysFont(name='Comic Sans MS', size=15, bold=True)

clock = pygame.time.Clock()
FPS = 60
BG = (255, 255, 255)
run = True
from math import pi, cos, sin
def draw_bg():
    screen.fill(BG)

img_scale = 0.15
img_size = pygame.image.load(f'img/icons/forest.png').convert_alpha().get_width()*img_scale

t = Tile(200, 200, 'bricks', 6, GAME_FONT, img_size)
t1 = Tile(500, 500, 'cattle', 2, GAME_FONT, img_size)
t2 = Tile(700, 650, 'forest', 10, GAME_FONT, img_size)
t4 = Tile(700, 200, 'forest', 12, GAME_FONT, img_size)
while run:
    clock.tick(FPS)
    draw_bg()
    t.draw(screen)
    t2.draw(screen)
    t1.draw(screen)
    t4.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

                
    pygame.display.update()
pygame.quit()