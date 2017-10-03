# -*- coding: utf8 -*-
"""
flower.py - hoitaa kukkien käyttäytymisen

Sisältää:
class Flower - kukkien yleisobjekti
"""
import pygame
import groups
import random
import seed
from pygame.locals import *
from settings import *
from colors import *


class Flower(pygame.sprite.Sprite):
    class State(object):
        GROWING, FLOWER, SEED_POD, WITHERING = range(4)
        STALK_COLOR = [GREEN, (40, 230, 10), (80, 180, 20), BROWN]
    """
    """
    def __init__(self, x, y, parent=None, plot=None, main=None, initial_spawn=0):
        pygame.sprite.Sprite.__init__(self, groups.flower_group)
        # if Settings.DEBUG_TEXT: print "Spawning a flower..."

        # Paikka ruudukossa
        self.x = x
        self.y = y

        # GENOMI
        if parent is not None:
            self.genome = parent.genome.copy()
            self.life_counter = 0
        else:
            # Jos ei ole vanhempaa niin on initial spawnia - silloin luetaan asetuksista alkuarvot
            self.genome = Settings.flower_default_genome.copy()
            # Randomoidaan elinaika
            self.life_counter = random.randint(0, self.genome['lifetime'] - 1)

        # if Settings.DEBUG_TEXT: print "Genome:\n{}".format(self.genome)
        # Viittaukset maailmaan ja soluun
        self.parent = parent
        self.plot = plot
        self.main = main

        # Tärkeä - asetettaa solun kukaksi itsensä
        self.plot.flower = self

        # Väri
        self.color = GREEN

        # Ominaisuudet
        self.stalk_width = 1  # update_image laskee tämän uusiksi iän mukaan

        self.state = None
        self.seeds_sprouted = 0
        self.update_state()

        self.height = self.life_counter

        # Kuva, rect
        self.image = None
        self.rect = None
        self.update_image()


    def update_image(self):
        """ Päivittää kuvan ja rectin """
        if self.life_counter <= 5:
            self.stalk_width = 1
        else:
            self.stalk_width = 3

        self.color = Flower.State.STALK_COLOR[self.state]

        self.image = pygame.Surface((Settings.flower_gfx_width, self.height + 5))
        self.rect = self.image.get_rect()
        # print self.rect.bottom, self.rect.top
        stalk_bottom = self.rect.midbottom
        stalk_top = self.rect.midbottom[0], self.rect.midbottom[1] - self.height
        pygame.draw.line(self.image, self.color, stalk_bottom, stalk_top, self.stalk_width)
        if self.state == Flower.State.FLOWER:
            pygame.draw.circle(self.image, YELLOW, stalk_top, 5)
        elif self.state == Flower.State.SEED_POD:
            pygame.draw.circle(self.image, BROWN, stalk_top, 5)
        self.rect.midbottom = self.plot.rect.midbottom[0], self.plot.rect.midbottom[1] - Settings.plot_height

    def update_state(self):
        if self.life_counter < self.genome['growth_duration']:
            self.state = Flower.State.GROWING
        elif self.life_counter < self.genome['growth_duration'] + self.genome['flower_duration']:
            self.state = Flower.State.FLOWER
        elif self.life_counter < self.genome['growth_duration'] + self.genome['flower_duration'] + self.genome['seeds_grow_time']:
            self.state = Flower.State.SEED_POD
        else:
            self.state = Flower.State.WITHERING

    def kill(self):
        """
        Tappaa kukan. Eli:
            -poistaa sprite-ryhmästä
            -poistaa maailman flower citionarystä
            -poistaa solusta viittauksen
        """
        pygame.sprite.Sprite.kill(self)
        del self.main.flowers_dict[self.x][self.y]
        self.plot.flower = None

    def update(self):
        """
        Laskee elinaikaa. Jos liian kuuma/kylmä, elinaika lyhyempi. Jos elinaika täysi, kuolee.
        Myös lisää itsensä kukkalaskuriin.
        """
        # temp_diff = float(abs(self.world.cells_dict[self.x][self.y].temp - self.preferred_temp))
        self.life_counter += 1
        self.update_state()

        if self.state == Flower.State.GROWING:
            self.grow(1)

        if self.state == Flower.State.WITHERING and not self.seeds_sprouted:
            self.sprout_seeds()

        if self.life_counter >= self.genome['lifetime']:
            self.kill()
        else:
            self.update_image()

    def grow(self, amount):
        self.height += amount

    def sprout_seeds(self):
        for i in range(int(self.genome['seeds_number'])):
            new_x = random.randint(int(self.x - self.genome['seeds_distance']),
                                   int(self.x + self.genome['seeds_distance']))
            new_y = random.randint(int(self.y - self.genome['seeds_distance']),
                                   int(self.y + self.genome['seeds_distance']))

            try:
                seed.Seed(new_x, new_y, parent=self, main=self.main)
            except KeyError:
                print "Couldn't sprout seeds outside grid: {}, {}".format(new_x, new_y)
                pass

