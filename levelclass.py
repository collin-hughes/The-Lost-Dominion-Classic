"""Collin Hughes: Primary Designer and Coder"""
import pygame
import pytmx
import random
import settings
from os import path

class Level:
    def __init__(self, mapfile):
        """Loads the map for pygame and defines the pixel width and height of the map"""
        self.tmxdata = pytmx.load_pygame(mapfile, pixelaplha = True)
        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight

    def render_map(self, surface):
        """Loads x, y and image for each tile on the map"""
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
                if isinstance(layer, pytmx.TiledTileLayer):
                    for x, y, gid, in layer:
                        tile = ti(gid)
                        if tile:
                            surface.blit(tile, (x * self.tmxdata.tilewidth,
                                                y * self.tmxdata.tileheight))

    def make_map(self):
        """Creates the map on the screen"""
        self.map = pygame.Surface((self.width, self.height))
        self.render_map(self.map)
        return self.map
