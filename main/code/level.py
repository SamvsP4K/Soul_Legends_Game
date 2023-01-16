import pygame
from settings import *
from tile import Tile
from player import Player
from support import *
from random import choice
from weapon import Weapon

PLAYER_STARTING__POS_X = 1975
PLAYER_STARTING_POS_Y = 1430
TILESIZE = 64
#creating two sprite groups
class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprits = YsortCameraGroup()
        self.obstacle_sprits = pygame.sprite.Group()

        self.current_attack = None

        #sprite setup
        self.create_map()


    #drawing objects to world map
    def create_map(self):
        layout ={
            "boundary":import_csv_layout("map/map_FloorBlocks.csv"),
            "grass":import_csv_layout("map/map_Grass.csv"),
            "object":import_csv_layout("map/map_LargeObjects.csv")
        }

        graphics = {
            "grass": import_folder("graphics/grass"),
            "object": import_folder("graphics/objects")
        }

        
        for style, layout in layout.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        #creates map invisible boundary
                        if style == "boundary":
                            Tile((x,y),[self.obstacle_sprits] ,"invisible")
                        #creates grass tiles
                        if style == "grass":
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y),[self.visible_sprits,self.obstacle_sprits],"grass", random_grass_image)
                        #creates object tiles
                        if style == "object":
                            surf = graphics["object"][int(col)]
                            Tile((x,y),[self.visible_sprits,self.obstacle_sprits],"object", surf)

            self.player = Player((PLAYER_STARTING__POS_X,PLAYER_STARTING_POS_Y),[self.visible_sprits], self.obstacle_sprits,self.create_attack,self.destroy_attack)

    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprits])
    
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None


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

        #creating the floor
        self.floor_surf = pygame.image.load("graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft =(0,0))

    def custom_draw(self,player):
        #creating camera offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

