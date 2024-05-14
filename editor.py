import sys

import pygame

from scripts.utils import load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0

class Editor:
    def __init__(self):
        # initialize pygame
        pygame.init()
        pygame.display.set_caption("Editor")

        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        self.assets = {
            "decor": load_images("tiles/decor"),
            "grass": load_images("tiles/grass"),
            "large_decor": load_images("tiles/large_decor"),
            "stone": load_images("tiles/stone"),
        }
        self.movement = [False, False, False, False]

        self.tilemap = Tilemap(self, tile_size=16)
        self.scroll = [0, 0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True

    def run(self):

        while True:
            self.display.fill((0, 0, 0))

            self.scroll[0] += (self.movement[0] - self.movement[1]) * 2
            self.scroll[1] += (self.movement[2] - self.movement[3]) * 2

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            m_pos = pygame.mouse.get_pos()
            m_pos = (m_pos[0] / RENDER_SCALE, m_pos[1] / RENDER_SCALE)

            tile_pos = (
                int((m_pos[0] + self.scroll[0]) // self.tilemap.tile_size),
                int((m_pos[1] + self.scroll[1]) // self.tilemap.tile_size),
            )

            self.display.blit(
                current_tile_img,
                (
                    tile_pos[0] * self.tilemap.tile_size - self.scroll[0],
                    tile_pos[1] * self.tilemap.tile_size - self.scroll[1],
                )
            )

            if self.clicking:
                self.tilemap.tilemap[str(tile_pos[0]) + ";" + str(tile_pos[1])] = {
                    "type": self.tile_list[self.tile_group],
                    "variant": self.tile_variant,
                    "pos": tile_pos
                }

            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ";" + str(tile_pos[1])

                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]

            self.display.blit(current_tile_img, (5, 5))

            # gets events to ensure that there is input if it is not written the cursor will be loading
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True

                    if event.button == 3:
                        self.right_clicking = True

                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])

                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])

                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0

                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False

                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN:  # if a given key is pressed
                    if event.key == pygame.K_a:
                        self.movement[0] = True  # Move left

                    if event.key == pygame.K_d:
                        self.movement[1] = True  # Move right

                    if event.key == pygame.K_w:
                        self.movement[2] = True  # Move up

                    if event.key == pygame.K_s:
                        self.movement[3] = True  # Move down

                    if event.key == pygame.K_LSHIFT:
                        self.shift = True

                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid

                if event.type == pygame.KEYUP:  # if a given key is released
                    if event.key == pygame.K_a:
                        self.movement[0] = False

                    if event.key == pygame.K_d:
                        self.movement[1] = False

                    if event.key == pygame.K_w:
                        self.movement[2] = False

                    if event.key == pygame.K_s:
                        self.movement[3] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            pygame.display.update()
            self.clock.tick(60)


Editor().run()
