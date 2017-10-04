# -*- coding: utf8 -*-
"""
text.py - hoitaa tekstin näytön ruudulla

Sisältää:
class Text - tekstiobjekti
"""
import pygame

DEBUG_TEXT = 0


class Text(pygame.sprite.Sprite):
    """ Näyttää tekstin ruudulla """
    def __init__(self, group=None, pos=None, text="", text_color=(255, 255, 255), bgcolor=(0, 0, 0), font_size=24,
                 align='center', visible=1):
        pygame.sprite.Sprite.__init__(self, group)
        self._pos = pos
        self._text = text
        self._text_color = text_color
        self._bgcolor = bgcolor
        self._font_size = font_size
        self._align = align
        self._visible = visible

        self._font = pygame.font.SysFont("couriernew", self._font_size, bold=True)
        self.image = None
        self.rect = None
        self._visible_image = None
        self._visible_rect = None
        self._not_visible_image = pygame.Surface((0, 0))
        self._not_visible_rect = pygame.Rect(0, 0, 0, 0)
        self._rendered_text = None

        self._render_text()
        self._set_visible(self._visible)

        #print self.image, self.rect

    def _render_text(self):
        # print "Rendering text: \"{}\"".format(self.text)
        self._visible_image = self._font.render(self._text, 1, self._text_color, self._bgcolor)
        self._rendered_text = self._text
        self._update_rect()
        self._set_visible(self._visible)

    def _get_text(self):
        return self._text

    def _set_text(self, text):
        # print "Setting text:  \"{}\"".format(text)
        self._text = str(text)
        self._render_text()

    def _get_pos(self):
        return self._pos

    def _set_pos(self, pos):
        self._pos = pos
        self._update_rect()

    def _update_align(self):
        if DEBUG_TEXT: print "_update_align in Text {}".format(self._text)
        if self._align == 'center':
            self._visible_rect.center = self._pos
        elif self._align == 'topleft':
            self._visible_rect.topleft = self._pos
        elif self._align == 'topright':
            self._visible_rect.topright = self._pos
        elif self._align == 'bottomleft':
            self._visible_rect.bottomleft = self._pos
        elif self._align == 'midbottom':
            self._visible_rect.midbottom = self._pos
        elif self._align == 'bottomright':
            self._visible_rect.bottomright = self._pos

    def _update_rect(self):
        self._visible_rect = self._visible_image.get_rect()
        self._update_align()
        if DEBUG_TEXT: print "Updated rect in Text {}".format(self._text)
        if DEBUG_TEXT: print "New rect: {}".format(self.rect)
        if DEBUG_TEXT: print "pos: {}".format(self._pos)

    def _get_visible(self):
        return self._visible

    def _set_visible(self, visible):
        self._visible = visible
        if visible == 1:
            self.image = self._visible_image
            self.rect = self._visible_rect
        else:
            self.image = self._not_visible_image
            self.rect = self._not_visible_rect
        # self._update_rect()

    def update(self):
        pass

    text = property(_get_text, _set_text)
    pos = property(_get_pos, _set_pos)
    visible = property(_get_visible, _set_visible)
