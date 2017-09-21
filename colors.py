# -*- coding: utf8 -*-
"""
colors.py - hoitaa väreihin liittyviä juttuja

Sisältää:
väri-constantteja
funktio number_to_color - muuttaa numeron väriarvoksi
"""
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (165, 42, 42)
DIRTBROWN = (87, 59, 12)
YELLOWISH = (212, 208, 100)
NEW_BLACK = (0, 0, 1)
ORANGE = NEW_BLACK


def number_to_color(number):
    """
    Ottaa vastaan numeron väliltä 0-100
    Palauttaa väriarvon tuplena (R,G,B)
    Liukuma: sininen (0) - punainen (100)
    """
    # brightness_adj = 50
    number = int(number)
    number = max(0, number)
    number = min(100, number)
    red_component = round(number * 2.55)
    green_component = 0
    blue_component = 255 - round(number * 2.55)
    return red_component, green_component, blue_component

