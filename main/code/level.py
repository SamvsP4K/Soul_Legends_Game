import pygame
from settings import *
from tile import Tile
from player import Player

#creating two sprite groups
class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprits = pygame.sprite.Group()
        self.obstacle_sprits = pygame.sprite.Group()

        #sprite setup
        self.create_map()

    #drawing objects to world map
    def create_map(self):
        for row_index,row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == "x":
                    Tile((x,y),[self.visible_sprits,self.obstacle_sprits])
                if col == "p":
                    Player((x,y),[self.visible_sprits])

            #print(row_index)
            #print(row)


    def run(self):
        #update and draw game
        self.visible_sprits.draw(self.display_surface)