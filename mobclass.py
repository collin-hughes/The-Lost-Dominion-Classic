'''Alex Schwartzberg: Primary Designer and Coder'''
import pygame
import random
import math
import settings
from playerclass import Player
vec = pygame.math.Vector2


class Mob(pygame.sprite.Sprite):
	def __init__(self, game, x_start, y_start, health, attackStrength):
		'''Initializes the spawn location as well as vectors for mob to follow player with in this method'''
		self.groups = game.all_sprites, game.mobs
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = game.mob_img
		self.rect = self.image.get_rect()
		self.rect.centerx = x_start * settings.TILESIZE
		self.rect.bottom = y_start * settings.TILESIZE
		self.pos = vec(self.rect.centerx, self.rect.bottom)
		self.vel = vec(0,0)
		self.acc = vec(0,0)
		self.rect.center = self.pos
		self.hp = health
		self.speed = 15
		self.attackStrength = attackStrength
		self.rot = 0

	def update(self):
		'''Allows for the mob to follow the direction and location of the player'''
		self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
		self.image = pygame.transform.rotate(self.game.mob_img, self.rot)
		self.rect = self.image.get_rect()
		self.rect.center = self.pos
		self.acc = vec(50,0).rotate(-self.rot)
		self.acc += self.vel * -1
		self.vel += self.acc * self.game.dt
		self.pos += self.vel * self.game.dt + (0.5 * self.acc * self.game.dt ** 2)
		
