import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        direction = player.status.split("_")[0]

        #weapon graphics
        self.image = pygame.Surface((40,40))

        #weapon placement
        if direction == "right":
            self.rect = self.image.get_rect(midleft = player.rect.midright)
        else:
            self.rect = self.image.get_rect(center = player.rect.center)