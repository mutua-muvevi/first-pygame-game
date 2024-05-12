import sys

import pygame


class Game:
	def __init__(self):
		# initialize pygame
		pygame.init()
		pygame.display.set_caption("The Ninja Game")

		self.screen = pygame.display.set_mode((640, 480))
		self.clock = pygame.time.Clock()

		self.img = pygame.image.load("data/images/clouds/cloud_1.png")
		self.img.set_colorkey((0, 0, 0))
		self.img_pos = [160, 260]

		self.movement = [False, False]

		self.collision_area = pygame.Rect(50, 50, 300, 50)

	def run(self):

		while True:
			self.screen.fill((14, 219, 248))

			img_r = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height())

			if img_r.colliderect(self.collision_area):
				pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area)
			else:
				pygame.draw.rect(self.screen, (0, 50, 155), self.collision_area)

			self.img_pos[1] += (self.movement[1] - self.movement[0]) * 5  # multiply increases the speed
			self.screen.blit(self.img, self.img_pos)  # loads the image to screen using blit

			# gets events to ensure that there is input if it is not written the cursor will be loading
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:  # if a given key is pressed
					if event.key == pygame.K_UP:
						self.movement[0] = True

					if event.key == pygame.K_DOWN:
						self.movement[1] = True

				if event.type == pygame.KEYUP:  # if a given key is released
					if event.key == pygame.K_UP:
						self.movement[0] = False

					if event.key == pygame.K_DOWN:
						self.movement[1] = False



			pygame.display.update()
			self.clock.tick(60)


Game().run()
