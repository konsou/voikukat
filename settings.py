# -*- coding: utf8 -*-
"""
settings.py - hoitaa asetukset

Sisältää:
class Settings - sisältää asetuksia
"""


class Settings(object):
    DEBUG_TEXT = 1

    # Solujen määrä, koko, ominaisuudet
    plots_x = 50
    plots_y = 10
    plot_width = 20
    plot_height = 5
    plot_space_for_flower = 40

    # Mutaatiovakio
    MUTATION_CONSTANT = 0.2  # prosentteina - eli 1.0 = 100%

    # Kukkien ominaisuudet - alkuarvot
    flower_gfx_width = 10
    flower_default_genome = {
        'lifetime': 30.0,
        'growth_per_turn': 1.0,
        'growth_duration': 10.0,
        'flower_duration': 5.0,
        'seeds_grow_time': 5.0,
        'seeds_distance': 5.0,
        'seeds_number': 6.0,
    }

    # siementen ominaisuudet - alkuarvot
    seed_grow_time = 5.0

    # Ikkunan koko
    window_margin = 100
    window_size = (plots_x * plot_width + 2 * window_margin, plots_y * (plot_height + plot_space_for_flower) + 2 * window_margin)
    window_center_point = window_size[0] // 2, window_size[1] // 2
    window_caption = "Flowers"

    # FPS, vuoroajastin
    fps = 30
    turn_time_seconds = 0.5
