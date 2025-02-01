import pygame

from math import pi, cos, sin
import pygame.gfxdraw
from pygame import Color
from utils.Tile import *

img_scale = 0.15
img_size = 153.6

board_info = [
    [{'type':'bricks','tile_num':8}, {'type':'forest','tile_num':10}, {'type':'cattle','tile_num':3}],
    [{'type':'forest','tile_num':11}, {'type':'wheat','tile_num':9}, {'type':'stone','tile_num':8}, {'type':'wheat','tile_num':3}],
    [{'type':'cattle','tile_num':9}, {'type':'stone','tile_num':5}, {'type':'cattle','tile_num':12}, {'type':'cattle','tile_num':9}, {'type':'forest','tile_num':6}],
    [{'type':'desert','tile_num':10}, {'type':'bricks','tile_num':3}, {'type':'wheat','tile_num':6}, {'type':'bricks','tile_num':11}],
    [{'type':'stone','tile_num':4}, {'type':'forest','tile_num':5}, {'type':'wheat','tile_num':4}]
]

class BaseBoard:

    def __init__(self, board_cent_pos, board_colour, tile_size, game_font, radius=500):
        self.x_c = board_cent_pos[0]
        self.y_c = board_cent_pos[1]
        self.board_background = Hexagon(board_cent_pos, radius)
        self.game_font = game_font
        self.tile_size = tile_size
        self.tile_rad = self.tile_size[1]/2+7
        self.board_colour = board_colour
        self.tiles = []
        tile_row_pos = self.get_tiles_row_start_positions(5)
        for i, tiles_row in enumerate(board_info): #TODO change this board info to be read from some config file
            self.generate_tiles(tile_row_pos[i], tiles_row)
        

    def get_tiles_row_start_positions(self, n):
        tile_row_pos = []
        for i in range(n):
            dx = -(i+2) if i<=n//2 else i-n-1
            dy = n//2 - i
            x_row = self.x_c + dx*cos(pi/6)*self.tile_rad 
            y_row = self.y_c + dy*(1+sin(pi/6))*self.tile_rad
            tile_row_pos.append((x_row, y_row))
        return tile_row_pos

    def draw(self, surf):
        self.board_background.draw(surf, self.board_colour)
        self.draw_tiles(surf)

    def draw_tiles(self, surf):
        for t in self.tiles:
            t.draw(surf)

    def generate_tiles(self, first_tile_cord, tiles_info):
        for i in range(len(tiles_info)):
            t_info = tiles_info[i]
            t_type = t_info['type']
            t_num = t_info['tile_num']
            t_size = img_size
            x_cord = first_tile_cord[0]+2*i*cos(pi/6)*self.tile_rad
            y_cord = first_tile_cord[1]

            new_tile = Tile((x_cord, y_cord), t_type, t_num, self.game_font, self.tile_size)
            self.tiles.append(new_tile)