"""Dylan Van Manen: Primary Designer, Collin Hughes: Coder"""
import pygame
from settings import *

class Hitbox(pygame.sprite.Sprite):
  def __init__(self, spawn):
    pygame.sprite.Sprite.__init__(self)
    self.hitbox = pygame.Surface((24, 32))
    self.rect = self.hitbox.get_rect()
    self.rect.midleft = spawn
