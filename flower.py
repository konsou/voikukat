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
        GROWING, FLOWER, SEED_POD, WITHERING, DYING = range(5)
        STALK_COLOR = [GREEN, (40, 230, 10), (80, 180, 20), BROWN, DIRTBROWN]

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
            # Base energy
            self._base_energy = parent.energy
        else:
            # Jos ei ole vanhempaa niin on initial spawnia - silloin luetaan asetuksista alkuarvot
            self.genome = Settings.flower_default_genome.copy()
            # Randomoidaan elinaika
            self.life_counter = random.randint(0, self.genome['lifetime'] - 1)
            # Base energy
            self._base_energy = self.genome['energy_cost_per_seed']

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
        self._energy = self._base_energy

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
        stalk_top = self.rect.midbottom[0], self.rect.midbottom[1] - int(self.height)
        pygame.draw.line(self.image, self.color, stalk_bottom, stalk_top, self.stalk_width)
        if self.state == Flower.State.FLOWER:
            pygame.draw.circle(self.image, YELLOW, stalk_top, 5)
        elif self.state == Flower.State.SEED_POD:
            pygame.draw.circle(self.image, BROWN, stalk_top, 5)
        self.rect.midbottom = self.plot.rect.midbottom[0], self.plot.rect.midbottom[1] - Settings.plot_height

    def update_state(self):
        if self.state != Flower.State.DYING:
            if self.life_counter <= self.genome['growth_duration']:
                self.change_state(Flower.State.GROWING)
            elif self.life_counter <= self.genome['growth_duration'] + self.genome['flower_duration']:
                self.change_state(Flower.State.FLOWER)
            elif self.life_counter <= self.genome['growth_duration'] + self.genome['flower_duration'] + self.genome['seeds_grow_time']:
                self.change_state(Flower.State.SEED_POD)
            else:
                self.change_state(Flower.State.WITHERING)

    def change_state(self, state):
        """
        Tämä händlää statejen vaihdon. Jos staten vaihto vaatii energiaa niin se toteutuu vain jos energiaa on riittävästi.
        """
        # Vaihdetaan statea vain jos se olisi oikeasti staten vaihtoa
        if self.state != state:
            state_change_ok = 1
            if state == Flower.State.FLOWER:
                if self.energy >= self.genome['energy_cost_flower']:
                    self.energy -= self.genome['energy_cost_flower']
                else:
                    # Ei energiaa kukkimiseen!
                    state_change_ok = 0

            if state_change_ok:
                self.state = state

    def kill(self):
        """
        Tappaa kukan. Eli:
            -poistaa sprite-ryhmästä
            -poistaa maailman flower citionarystä
            -poistaa solusta viittauksen
        """
        pygame.sprite.Sprite.kill(self)
        self.main.flowers_dict[self.x][self.y] = None
        self.plot.flower = None

    def cut_down(self, cut_height):
        if self.height > cut_height:
            self.state = Flower.State.DYING

    def update(self):
        """
        Laskee elinaikaa. Jos liian kuuma/kylmä, elinaika lyhyempi. Jos elinaika täysi, kuolee.
        Myös lisää itsensä kukkalaskuriin.
        """

        if self.state == Flower.State.DYING:
            self.life_counter += 2
        else:
            self.life_counter += 1

        self.gather_energy()
        self.energy_maintenance()
        self.update_state()

        if self.state == Flower.State.GROWING:
            self.grow()

        if self.state == Flower.State.WITHERING and not self.seeds_sprouted:
            self.sprout_seeds()

        if self.life_counter >= self.genome['lifetime']:
            self.kill()
        else:
            self.update_image()

    def energy_maintenance(self):
        energy_cost = 0
        if self.state == Flower.State.FLOWER:
            energy_cost += self.genome['energy_cost_maint_flower']
        elif self.state == Flower.State.SEED_POD:
            energy_cost += self.genome['energy_cost_maint_seedpod']

        energy_cost += self.height * self.genome['energy_cost_maint_per_height']

        self.energy -= energy_cost

        if self.energy < 0:
            self.change_state(Flower.State.DYING)


    def gather_energy(self):
        self.energy += self.height * self.genome['energy_gain_per_height']

    def grow(self):
        """ Kasvattaa itseään jos siihen on energiaa """
        if self.energy >= self.genome['energy_cost_grow']:
            self.height += self.genome['growth_per_turn']
            self.energy -= self.genome['energy_cost_grow']

    def sprout_seeds(self):
        """ Viskoo siemeniä niin paljon kuin energiaa riittää """
        self.seeds_sprouted = 1

        while True:
        # for i in range(int(self.genome['seeds_number'])):
            new_x = random.randint(int(self.x - self.genome['seeds_distance']),
                                   int(self.x + self.genome['seeds_distance']))
            new_y = random.randint(int(self.y - self.genome['seeds_distance']),
                                   int(self.y + self.genome['seeds_distance']))

            if self.energy >= self.genome['energy_cost_per_seed']:
                # Energiaa on, spawnataan siemen
                seed.Seed(new_x, new_y, parent=self, main=self.main)
                self.energy -= self.genome['energy_cost_per_seed']
            else:
                # Energia loppu, ei spawnata enää
                break

    def _get_energy(self):
        return self._energy

    def _set_energy(self, value):
        self._energy = min(value, self.energy_storage)

    def _get_energy_storage(self):
        return self.height * self.genome['energy_storage_per_height'] + self._base_energy

    energy = property(_get_energy, _set_energy)
    energy_storage = property(_get_energy_storage)