import pygame 
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("graphics/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        #adding player hitbox
        self.hitbox = self.rect.inflate(0,-26)

        #player movement and obstacle collision
        self.direction = pygame.math.Vector2()
        self.speed = 5
        
        self.obstacle_sprite = obstacle_sprites

        #movement keys
    def input(self):
        keys = pygame.key.get_pressed()
        #up and down movements
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        #right and left movements
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collison("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collison("vertical")
        self.rect.center = self.hitbox.center
    

    def collison(self,direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #if player is moved to the right and collides with obstacle, player gets pushed back to the left
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: #if player is moved to the left and collides with obstacle, player gets pushed back to the right
                        self.hitbox.left = sprite.hitbox.right
                        
        #vertical collisions follow the same logic as above horizontal collisions except on Y axis 
        if direction == "vertical":
            for sprite in self.obstacle_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: 
                        self.hitbox.top = sprite.hitbox.bottom
    
    def update(self):
        self.input()
        self.move(self.speed)