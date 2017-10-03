# -*- coding: utf8 -*-

import pygame
import groups
import flower
import seed
from settings import *
from colors import *


class Plot(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None, main=None):
        pygame.sprite.Sprite.__init__(self, groups.plot_group)

        self.main = main

        self.x = x
        self.y = y

        self.width = Settings.plot_width
        self.height = Settings.plot_height + Settings.plot_space_for_flower
        self.gfx_height = Settings.plot_height

        self.image = None
        self.update_image()
        self.rect = self.image.get_rect()

        self.rect.topleft = (Settings.window_margin + self.x * Settings.plot_width,
                             Settings.window_margin + self.y * (Settings.plot_height + Settings.plot_space_for_flower))

        # Tätä käytetään hoveroinnin käsittelyssä
        self.mouse_is_over = 0

        self.flower = None
        self.seeds = []

    def update(self):
        pass
        # if self.flower is None:
        #     self.flower = flower.Flower(self.x, self.y, plot=self, main=self.main)
        #     self.main.flowers_dict[self.x][self.y] = self.flower

    def update_image(self):
        self.image = pygame.Surface((self.width, self.height))
        pygame.draw.rect(self.image, DIRTBROWN, (0, self.height - self.gfx_height, self.width, self.gfx_height))

    def handle_mouse_motion(self, event):
        """
        Ottaa vastaan pygamen mouse motion -eventin.
        Jos hiiri osuu itseen niin kutsuu mouse_enter()-metodia ja palauttaa itsensä.
        Muussa tapauksessa kutsuu mouse_exit()-metodia ja palauttaa None.
        """
        ret_val = None
        if self.rect.collidepoint(event.pos):
            self.mouse_enter()
            ret_val = self
        else:
            self.mouse_exit()
        return ret_val

    def handle_mouse_click(self, event):
        """
        Ottaa vastaan pygamen mouse click -eventin.
        Luo seedin
        """
        if self.rect.collidepoint(event.pos):
            if event.button == 1:
                seed.Seed(self.x, self.y, main=self.main)
            elif event.button == 3:
                pass

    def mouse_enter(self):
        """ Käsitellään tilanne kun hiiri tulee solun päälle - muuttaa väriä """
        if not self.mouse_is_over:
            self.mouse_is_over = 1
            self.image.fill(YELLOWISH)
            # return "x: {} y: {} temp: {}".format(self.x, self.y, round(self.temp, 2))

    def mouse_exit(self):
        """ Käsitellään tilanne kun hiiri on poissa solun päältä - palautetaan väri alkuperäiseksi """
        if self.mouse_is_over:
            self.mouse_is_over = 0
            self.update_image()
