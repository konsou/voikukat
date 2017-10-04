# -*- coding: utf8 -*-
"""
groups.py - hoitaa pygamen sprite-ryhmät
"""
import pygame
import numpy


class CustomGroup(pygame.sprite.Group):
    def __init__(self):
        print "__init__ new CustomGroup"
        pygame.sprite.Group.__init__(self)

    def get_avg_max_height(self):
        height_list = []
        for spr in self.sprites():
            height_list.append(int(spr.genome['growth_duration']) * spr.genome['growth_per_turn'])
        return numpy.mean(height_list)

    def get_avg_lifetime(self):
        lifetime_list = []
        for spr in self.sprites():
            lifetime_list.append(spr.genome['lifetime'])
        return numpy.mean(lifetime_list)


# Groupit
plot_group = pygame.sprite.Group()
flower_group = CustomGroup()
seed_group = CustomGroup()
ui_group = pygame.sprite.Group()
