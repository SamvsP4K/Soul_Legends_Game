import pygame 
from settings import *
from support import import_folder
from support import weapon_data

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites,create_attack,destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load("graphics/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)

        #graphics setup and retreving player status for animation
        self.import_player_assets()
        self.status = "down"
        self.frame_index = 0
        self.animation_speed = 0.15

        #adding player hitbox
        self.hitbox = self.rect.inflate(0,-26)

        #player movement and obstacle collision
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprite = obstacle_sprites

        #weapon management
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]


        #asset imports for player animations
    def import_player_assets(self):
        character_path = "graphics/player/"
        self.animations = {"up":[],"down":[],"left":[],"right":[],
                            "right_idle":[],"left_idle":[],"up_idle":[],"down_idle":[],
                            "right_attack":[],"left_attack":[],"up_attack":[],"down_attack":[]}

        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

        #movement input keys and status
    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = "right"
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0

            #attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                print("attack")
            #magic input
            if keys[pygame.K_r]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print("magic")

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        #adding attack time so cannot be spammed
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        #pulling in animation based on player status
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"
        
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                if "idle" in self.status:
                    self.status.replace("_idle","+ _attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack","")

    
    #animates character by looping through folder animations
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)







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
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        