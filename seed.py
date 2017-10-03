# -*- coding: utf8 -*-
import pygame
import groups
import random
import flower
from pygame.locals import *
from settings import *
from colors import *
from settings import *


class Seed(pygame.sprite.Sprite):
    def __init__(self, x, y, parent=None, main=None, initial_spawn=0):
        pygame.sprite.Sprite.__init__(self, groups.seed_group)
        if Settings.DEBUG_TEXT: print "Spawning seed..."
        # GENOMI
        if parent is not None:
            # Kopioidaan vanhemman genomi
            self.genome = parent.genome.copy()
            # Mutatoidaan sitä
            self.mutate_genome()
            self.life_counter = 0
        else:
            # Jos ei ole vanhempaa niin on initial spawnia - silloin luetaan asetuksista alkuarvot
            self.genome = Settings.flower_default_genome.copy()
            # Randomoidaan elinaika
            self.life_counter = random.randint(0, self.genome['lifetime'] - 1)

        # Viittaukset maailmaan ja soluun ja vanhempaan
        self.plot = main.plots_dict[x][y]
        self.main = main
        self.parent = parent

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

        # Paikka ruudukossa
        self.x = x
        self.y = y

    def kill(self):
        """
        Tappaa siemenen. Eli:
            -poistaa sprite-ryhmästä
            -poistaa solusta viittauksen
            -jos solussa ei ole kukkaa niin spawnaa sellaisen
        """
        pygame.sprite.Sprite.kill(self)
        self.plot.seeds.remove(self)
        if self.plot.flower is None:
            flower.Flower(self.x, self.y, parent=self, plot=self.plot, main=self.main)

    def update(self):
        """
        Laskee elinaikaa.
        """
        self.life_counter += 1

        if self.life_counter >= self.genome['lifetime']:
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
