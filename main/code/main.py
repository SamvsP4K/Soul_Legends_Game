import pygame, sys
#from settings import *
from level import Level
import os
#sets the working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#pygame display settings
WIDTH    = 1280	
HEIGTH   = 720
FPS      = 60
TILESIZE = 64

#from debug import debug
class Game:
	def __init__(self):
		  
		# general pygame setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('Soul Legends')
		self.clock = pygame.time.Clock()
		self.level = Level()
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.screen.fill('black')
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()	



