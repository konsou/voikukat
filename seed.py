# -*- coding: utf8 -*-
import pygame
import groups
import random
import flower
from pygame.locals import *
from settings import *
from colors import *
from settings import *

# TODO: Siemenellä pitää olla energiavaranto jonka spawnaava kukka perii


class Seed(pygame.sprite.Sprite):
    def __init__(self, x, y, parent=None, main=None, initial_spawn=0):
        # if Settings.DEBUG_TEXT: print "Spawning seed at coordinates: x: {}, y: {}".format(x, y)

        # Viittaukset maailmaan ja soluun ja vanhempaan
        try:
            # Tämä aiheuttaa KeyErrorin jos yritetään spawnata ruudukon ulkopuolelle
            self.plot = main.plots_dict[x][y]
            continue_init = 1
        except KeyError:
            continue_init = 0
            # print "Seed outside play area (x: {}, y: {}). Skipping init.".format(x, y)

        if continue_init:
            pygame.sprite.Sprite.__init__(self, groups.seed_group)

            self.main = main
            self.parent = parent

            # Paikka ruudukossa
            self.x = x
            self.y = y

            # GENOMI
            if parent is not None:
                # Kopioidaan vanhemman genomi
                self.genome = parent.genome.copy()
                # Siemenen energiavaranto
                self.energy = parent.genome['energy_cost_per_seed']
                # Mutatoidaan sitä
                self.mutate_genome()
                self.life_counter = 0
            else:
                # Jos ei ole vanhempaa niin on initial spawnia - silloin luetaan asetuksista alkuarvot
                self.genome = Settings.flower_default_genome.copy()
                # Randomoidaan elinaika
                self.life_counter = random.randint(0, self.genome['seed_lifetime'] - 1)
                # Siemenen energiavaranto
                self.energy = self.genome['energy_cost_per_seed']

            # Tärkeä - lisäää soluun itsensä
            self.plot.seeds.append(self)

            # Väri
            self.color = BROWN

            # Kuva, rect
            self.height = 3
            self.width = 3
            self.image = pygame.Surface((self.width, self.height))
            self.rect = self.image.get_rect()
            pygame.draw.circle(self.image, self.color, self.rect.center, 2)
            self.rect.midbottom = self.plot.rect.midbottom[0], self.plot.rect.midbottom[1] - Settings.plot_height

            # print "__init__ finished. Has now image and rect: \n{} {}".format(self.image, self.rect)

    def __repr__(self):
        return "<Seed x: {}, y: {}, image: {}, rect: {}>".format(self.x, self.y, self.image, self.rect)

    def kill(self):
        """
        Tappaa siemenen. Eli:
            -poistaa sprite-ryhmästä
            -poistaa solusta viittauksen
            -jos solussa ei ole kukkaa niin spawnaa sellaisen
        """
        # print "Killing {}".format(self)
        pygame.sprite.Sprite.kill(self)
        self.plot.seeds.remove(self)
        # Kuollessa spawnaa kukan jos ruudussa ei jo ole
        if self.plot.flower is None:
            flower.Flower(self.x, self.y, parent=self, plot=self.plot, main=self.main)

    def update(self):
        """
        Laskee elinaikaa.
        """
        self.life_counter += 1

        if self.life_counter >= self.genome['seed_lifetime']:
            self.kill()

    def mutate_genome(self):
        """ Mutatoi genomia sopeutumisen aikaansaamiseksi """
        # if Settings.DEBUG_TEXT: print "Mutating genome:"
        # if Settings.DEBUG_TEXT: print self.genome
        new_genome = {}
        for item in self.genome:
            new_genome[item] = random.uniform(self.genome[item] - self.genome[item] * Settings.MUTATION_CONSTANT,
                                              self.genome[item] + self.genome[item] * Settings.MUTATION_CONSTANT)
        self.genome = new_genome
        # if Settings.DEBUG_TEXT: print self.genome
