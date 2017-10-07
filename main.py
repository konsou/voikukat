# -*- coding: utf8 -*-
"""
main.py - hoitaa itse ohjelman suorittamisen

sisältää:
class Program - ohjelmaobjekti
debug_run() - funktio, joka käynnistää ja ajaa ohjelman
"""
import pygame
import text
import groups
import plot
import flower
from pygame.locals import *
from colors import *
from settings import *


class Program(object):
    """
    Ohjelmaobjekti. Hoitaa seuraavat asiat:
        -Pygamen initit
        -graffojen piirrot
        -laskurien ja inffojen näyttö
        -eventtien handlaukset
        -lopettaminen

    Tätä on tarkoitus kutsua näin:
        game = Program()
        while game.running:
            game.update()
    """
    def __init__(self):
        # Pygamen inittiä, näytön asetus
        pygame.init()
        self.disp_surf = pygame.display.set_mode(Settings.window_size)
        pygame.display.set_caption(Settings.window_caption)

        self.clock = pygame.time.Clock()
        self.last_turn_started_at = pygame.time.get_ticks()

        self.running = 1

        # pause
        self.paused = 0
        self.paused_text = text.Text(group=groups.ui_group, pos=(Settings.window_center_point[0], Settings.window_size[1] - 10), font_size=40, text="PAUSED", align='midbottom', visible=0)

        self.turn_counter = 0
        self.lawnmower_every_x_turns = 50

        # hover_plot on se solu, jonka päällä hiiri on
        self.hover_plot = None

        # infotekstit
        self.turn_text = text.Text(group=groups.ui_group, pos=(30, 10), text="Turn 0", align='topleft')
        self.info_text = text.Text(group=groups.ui_group, pos=(Settings.window_size[0] - 30, 10), text="(info)", align='topright')
        self.info_text2 = text.Text(group=groups.ui_group, pos=(Settings.window_size[0] - 30, 40), text="(info2)", align='topright')
        self.info_text3 = text.Text(group=groups.ui_group, pos=(Settings.window_size[0] - 30, 70), text="(info3)", align='topright')
        self.info_text4 = text.Text(group=groups.ui_group, pos=(Settings.window_size[0] - 30, 100), text="(info4)", align='topright')
        # self.avg_temp_text = text.Text(group=groups.ui_group, pos=(Settings.window_size[0] - 30, 50), text="(avg tmp)", align='topright')
        self.flowers_counter_text = text.Text(group=groups.ui_group, pos=(Settings.window_size[0] - 40, Settings.window_size[1] - 50), text="(flowers)", align='bottomright')
        self.seeds_counter_text = text.Text(group=groups.ui_group, pos=(Settings.window_size[0] - 40, Settings.window_size[1] - 10), text="(seeds)", align='bottomright')
        self.avg_lifetime_text = text.Text(group=groups.ui_group, pos=(20, Settings.window_size[1] - 40), text="(lifetime)", align='bottomleft')
        self.avg_max_height_text = text.Text(group=groups.ui_group, pos=(20, Settings.window_size[1] - 10), text="(max height)", align='bottomleft')

        # Statsit
        self.stats_avg_temp = {}
        self.stats_black_flowers = {}
        self.stats_white_flowers = {}

        # Spawnataan plotit
        self.plots_dict = {}
        self.flowers_dict = {}

        for x in range(Settings.plots_x):
            self.plots_dict[x] = {}
            self.flowers_dict[x] = {}
            for y in range(Settings.plots_y):
                self.plots_dict[x][y] = plot.Plot(x=x, y=y, main=self)
                # self.flowers_dict[x][y] = flower.Flower(x=x, y=y, plot=self.plots_dict[x][y], initial_spawn=1, main=self)
                self.flowers_dict[x][y] = None

    def update(self):
        """
        update-metodi: tätä kun kutsutaan koko ajan niin ohjelma pyörii
        """
        # ruutu tyhjäksi
        self.disp_surf.fill(BLACK)

        # sprite-groupien piirrot ruudulle
        groups.plot_group.draw(self.disp_surf)
        groups.flower_group.draw(self.disp_surf)
        groups.seed_group.draw(self.disp_surf)
        groups.ui_group.draw(self.disp_surf)

        pygame.display.flip()

        self.clock.tick(Settings.fps)

        # eventtien handlaus
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = 0
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.running = 0
                elif event.key == K_SPACE:
                    self.pause()
                elif event.key == K_RETURN:
                    if self.paused:
                        self.advance_turn()
                elif event.key == K_RCTRL or event.key == K_LCTRL:
                    self.lawnmower()
                elif event.key == K_PLUS or event.key == K_KP_PLUS:
                    pass
                elif event.key == K_MINUS or event.key == K_KP_MINUS:
                    pass
            elif event.type == MOUSEMOTION:
                # heitetään mouse motion plottien käsiteltäväksi että osaavat muuttaa väriään jos hover
                for current_plot in groups.plot_group:
                    possible_hover_plot = current_plot.handle_mouse_motion(event)
                    if possible_hover_plot is not None:
                        self.hover_plot = possible_hover_plot
            elif event.type == MOUSEBUTTONDOWN:
                # heitetään mouse click myös plottien käsiteltäväksi - tällä hetkellä voi muuttaa lämpötilaa solussa näin
                for current_plot in groups.plot_group:
                    current_plot.handle_mouse_click(event)

        # hoveratun cellin infotekstin päivitys
        self.update_hover_text()

        # turn timen laskenta
        if not self.paused:
            if pygame.time.get_ticks() - self.last_turn_started_at >= Settings.turn_time_seconds * 1000:
                self.advance_turn()

    def lawnmower(self):
        for spr in groups.flower_group:
            spr.cut_down(Settings.lawnmower_height)

    def advance_turn(self):
        """
        Siirtää simulaation seuraavaan vuoroon. Käytännössä lähettää tästä vain tiedon world-objektille, joka
        hoitaa itse simuloinnin. Tämän jälkeen sitten päivittää infotekstit.
        """
        groups.plot_group.update()
        groups.flower_group.update()
        groups.seed_group.update()

        self.turn_counter += 1

        if self.turn_counter % self.lawnmower_every_x_turns == 0:
            self.lawnmower()

        # Päivitetään infotekstit
        self.turn_text.text = "Turn {}".format(self.turn_counter)
        # self.avg_temp_text.text = "Avg temp: {}".format(round(avg_temp, 2))
        self.flowers_counter_text.text = "Flowers: {}".format(len(groups.flower_group))
        self.seeds_counter_text.text = "Seeds: {}".format(len(groups.seed_group))
        self.avg_lifetime_text.text = "Avg lifetime: {}".format(groups.flower_group.get_avg_lifetime())
        self.avg_max_height_text.text = "Avg max height: {}".format(groups.flower_group.get_avg_max_height())

        # Turn counterin timerin nollaus
        self.last_turn_started_at = pygame.time.get_ticks()

    def update_hover_text(self):
        """ Päivittää sen infotekstin, joka kertoo hoveratun cellin tiedot """
        if self.hover_plot is not None and self.hover_plot.flower is not None:
            update_text = "height: {}, life: {}".format(self.hover_plot.flower.height, self.hover_plot.flower.life_counter)
            update_text2 = "seed_lifetime: {}, lifetime: {}, growth_per_turn: {}, growth_duration: {}".format(
                round(self.hover_plot.flower.genome['seed_lifetime'], 2),
                round(self.hover_plot.flower.genome['lifetime'], 2),
                round(self.hover_plot.flower.genome['growth_per_turn'], 2),
                round(self.hover_plot.flower.genome['growth_duration'], 2))
            update_text3 = "flower_duration: {}, seeds_grow_time: {}, seeds_distance: {}, seeds_number: {}".format(
                round(self.hover_plot.flower.genome['flower_duration'], 2),
                round(self.hover_plot.flower.genome['seeds_grow_time'], 2),
                round(self.hover_plot.flower.genome['seeds_distance'], 2),
                round(self.hover_plot.flower.genome['seeds_number'], 2))
            update_text4 = "energy: {}, energy_storage: {}".format(
                round(self.hover_plot.flower.energy, 2),
                round(self.hover_plot.flower.energy_storage, 2))
        else:
            update_text = ""
            update_text2 = ""
            update_text3 = ""
            update_text4 = ""

        self.info_text.text = update_text
        self.info_text2.text = update_text2
        self.info_text3.text = update_text3
        self.info_text4.text = update_text4

    def pause(self):
        if self.paused:
            self.paused = 0
            self.paused_text.visible = 0
        else:
            self.paused = 1
            self.paused_text.visible = 1


def debug_run():
    game = Program()
    while game.running:
        game.update()

if __name__ == "__main__":
    debug_run()