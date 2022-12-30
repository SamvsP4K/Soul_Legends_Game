import pygame
from settings import *
from tile import Tile
from player import Player

#creating two sprite groups
class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprits = YsortCameraGroup()
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
                    self.player = Player((x,y),[self.visible_sprits], self.obstacle_sprits)

            #print(row_index)
            #print(row)


    def run(self):
        #update and draw game
        self.visible_sprits.custom_draw(self.player)
        self.visible_sprits.update()

#camera setup
class YsortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self,player):
        #creating camera offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

