import pygame

from math import pi, cos, sin
import pygame.gfxdraw
from pygame import Color

class Ntagon:
    def __init__(self, n, center_position, radius, rotationAngle=0):
        self.x, self.y = center_position
        self.angle = 2*pi/n
        self.rotationAngle = rotationAngle
        self.points = []
        for i in range(n):
            xp = self.x + cos(self.angle*i+self.rotationAngle)*radius
            yp = self.y + sin(self.angle*i+self.rotationAngle)*radius
            self.points.append((xp, yp))
    
    def draw(self, surf, colour):
        pygame.gfxdraw.filled_polygon(surf, self.points, colour)

class Hexagon(Ntagon):
    def __init__(self, center_position, radius):
        super().__init__(6, center_position, radius, rotationAngle=pi/6)


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, t_type, tile_num, game_font, tile_size):
        pygame.sprite.Sprite.__init__(self)
        self.game_font = game_font
        self.tile_num = tile_num
        img = pygame.image.load(f'img/icons/{t_type}.png').convert_alpha()
        self.image = pygame.transform.scale(img, tile_size)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hexagon_side = int(tile_size[1]//2)
        dHexSide = 7
        self.hexagonFrame = Hexagon(self.rect.center, self.hexagon_side+dHexSide) #TODO check frame size



    def draw(self, surf):
        green_colour = (0, 255, 0)
        white_colour = (255, 255, 255)
        black_colour = (0, 0, 0)
        center_crl_r = 15
        self.hexagonFrame.draw(surf, white_colour)
        surf.blit(self.image, self.rect)
        cr = pygame.draw.circle(surf, white_colour, self.rect.center, center_crl_r)
        text_surf = self.game_font.render(str(self.tile_num), True, black_colour)
        text_rect = text_surf.get_rect(center = self.rect.center)
        surf.blit(text_surf, text_rect)
        
