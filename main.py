'''Colin Hughes: Primary Designer and Coder of GUI Logic, Bren Stace: Primary tester of code and editing of bugs,
Dylan Van Manen: Edits and constitutent of design process, Alex Schwartzberg: Added logic for loading data, events, and controlling models(made minor edits for efficiency)'''
#Imports
import pygame
import random
#import settings
from settings import *
from playerclass import *
from mobclass import *
from levelclass import *
from os import *
from hitboxclass import *
import os
import makestats
import highscore

class Game:
	def __init__(self):
		"""Initializes pygame, creates a screen and sets all variables that aren't reset"""
		pygame.init()
		pygame.mixer.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

		self.wave = 0
		self.amr = 0
		self.addspd = 0
		self.addmult = 0

		self.cheatcode = [273,273,274,274,276,275,276,275,98,97]
		self.newgame = [110,101,119,103,97,109,101]
		self.cheater = []

		self.all_sprites = pygame.sprite.Group()
		self.mobs = pygame.sprite.Group()

		pygame.display.set_caption("The Lost Dominion")
		self.clock = pygame.time.Clock()
		self.load_data()

	def load_data(self):
		"""Loads all game data"""
		# Loads folders
		game_folder = os.path.dirname(__file__)
		img_folder = os.path.join(game_folder, 'img')
		map_folder = path.join(path.dirname(__file__), "map")

		# Loads font
		self.font_name = pygame.font.match_font("algerian")

		# Loads images
		self.logo = pygame.image.load(os.path.join(img_folder, LOGO_IMG)).convert_alpha()
		self.logo = pygame.transform.scale2x(self.logo)
		self.player_img = pygame.image.load(os.path.join(img_folder, PLAYER_IMG)).convert_alpha()
		self.icon = pygame.image.load(os.path.join(img_folder, ICON)).convert_alpha()
		self.icon = pygame.transform.scale(self.icon, (128, 128))
		self.mob_img = pygame.image.load(os.path.join(img_folder, MOB_IMG)).convert_alpha()
		self.mob_icon = pygame.image.load(os.path.join(img_folder, MOB_ICON)).convert_alpha()
		self.mob_icon = pygame.transform.scale(self.mob_icon, (64, 64))

		# Renders the map
		self.map = Level(path.join(map_folder, 'arena1.tmx'))
		self.map_img = self.map.make_map()
		self.map_img = pygame.transform.scale(self.map_img, (WIDTH, HEIGHT))
		self.map_rect = self.map_img.get_rect()

	def movement(self):
		"""Contains all possible movement options"""
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_d] or keystate[pygame.K_RIGHT]:
			self.player.moveRight()
			self.player.pos = self.player.moveRightPos()
		if keystate[pygame.K_a] or keystate[pygame.K_LEFT]:
			self.player.moveLeft()
			self.player.pos = self.player.moveLeftPos()
		if keystate[pygame.K_s] or keystate[pygame.K_DOWN]:
			self.player.moveDown()
			self.player.pos = self.player.moveDownPos()
		if keystate[pygame.K_w] or keystate[pygame.K_UP]:
			self.player.moveUp()
			self.player.pos = self.player.moveUpPos()

	def draw_bar(self, surf, x, y, pct, orig_pct, bar_color):
		"""Draws a bar on the screen"""
		if pct < 0:
			pct = 0
		if pct != 0:
			fill = (pct / orig_pct) * BAR_LENGTH
			fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
			pygame.draw.rect(surf, bar_color, fill_rect)
		outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
		pygame.draw.rect(surf, BLACK, outline_rect, 2)

	def draw_text(self, surf, text, size, x, y, color):
		"""Writes text on the screen"""
		font = pygame.font.Font(self.font_name, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x, y)
		surf.blit(text_surface, text_rect)

	def attack(self):
		"""Everytime the player attacks it draws a hitbox that checks for a collision
		with a mob sprite and does damage"""
		attack_radius = Hitbox(self.player.rect.center)
		hits = pygame.sprite.spritecollide(attack_radius, self.mobs, False)
		if hits:
			for hit in hits:
				self.player.strike()
				hit.hp -= self.player.dmg
				self.update_text = "You attacked for " + str(int(self.player.dmg)) + " damage!"
				if hit.hp <= 0:
					hit.kill()
					self.mob_amt -= 1
					self.update_text = "You have slain a demon!"

	def get_hit(self):
		"""Checks to see if a mob has attacked the player and recieves damage"""
		hits = pygame.sprite.spritecollide(self.player, self.mobs, False)
		if hits:
			for hit in hits:
				self.player.amr -= self.mob.attackStrength
				if self.player.amr <= 0:
					self.player.amr = 0
					self.player.hp -= self.mob.attackStrength
				self.update_text = "You are taking damage!"
				if self.player.hp <= 0:
					self.player.kill()

	def set_boundaries(self):
		"""Defines the boundaries of the map"""
		if self.player.rect.right >= 46 * TILESIZE:
			self.player.rect.right = 46 * TILESIZE
		if self.player.rect.left <= 8 * TILESIZE:
			self.player.rect.left = 8 * TILESIZE
		if self.player.rect.bottom >= 24 * TILESIZE:
			self.player.rect.bottom = 24 * TILESIZE
		if self.player.rect.top <= 6 * TILESIZE:
			self.player.rect.top = 6 * TILESIZE

	def draw_enemies(self, surf, x, y, img):
		"""Draws the enemy heads on the screen"""
		for i in range(self.mob_amt):
			img_rect = img.get_rect()
			img_rect.x = x + (70 * i)
			img_rect.y = y
			surf.blit(img, img_rect)

	def create_enemies(self, x, y):
		"""Creates an enemy"""
		self.mob = Mob(self, x, y, makestats.makeHealth(self.wave), makestats.makeStrength(self.wave))
		self.all_sprites.add(self.mob)
		self.mobs.add(self.mob)

	def roll_stats(self):
		"""Rolls a stat boost at the end of the round"""
		end_of_wave_roll = random.randrange(1, 4)
		if(end_of_wave_roll == 1):
			self.player.amr += 25
			self.update_text = "The gods have granted you armor!"
		elif(end_of_wave_roll == 2):
			self.addspd += .3
			self.update_text = "The gods have made you faster!"
		else:
			self.addmult += .5
			self.update_text = "The gods have made you stronger!"

	def new(self):
		"""Starts a new iteration of the game"""
		self.player = Player(self, 9, 17, 100, 0, 1, 1)
		self.all_sprites.add(self.player)
		self.player.amr = self.amr
		self.roll_stats()
		self.player.spd += self.addspd
		self.player.multiplier += self.addmult
		self.maxamr = self.player.amr
		self.wave += 1

		# print(self.player.amr)
		# print(self.player.spd)
		# print(self.player.multiplier)
		# print(self.wave, "This is a new wave")

		self.high = highscore.check_high_score(self.wave)

		self.mob_amt = 9

		for i in range(self.mob_amt):
			if i % 2 != 0:
				x = 40
			else:
				x = 44
			self.create_enemies(x, 7 + (i * 2))


	def run(self):
		"""Runs the Game Loop"""
		self.playing = True
		self.new()
		while self.playing:
			self.dt = self.clock.tick(FPS)/1000 #For seconds
			self.events()
			self.update()
			self.draw()
			if self.mob_amt == 0:
				self.all_sprites.empty()
				self.amr = self.player.amr
				self.new()
			if self.player.hp <= 0:
				self.all_sprites.empty()
				self.mobs.empty()
				self.amr = 0
				self.addspd = 0
				self.addmult = 0
				self.playing = False


	def events(self):
		"""The events portion of the game loop; checks for key presses and anything that might happen in the game"""
		for event in pygame.event.get():
			# Check for closing the window
			if event.type == pygame.QUIT:
				exit()
			elif event.type == pygame.MOUSEBUTTONUP:
                                self.attack()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self.attack()
				if event.key == pygame.K_ESCAPE:
					self.all_sprites.empty()
					self.amr = 0
					self.addspd = 0
					self.addmult = 0
					self.playing = False
		self.movement()
		self.set_boundaries()
		self.get_hit()

	def update(self):
		"""The update portion of the game loop"""
		self.all_sprites.update()

	def draw(self):
		"""The draw portion of the game loop"""
		self.screen.blit(self.map_img, self.map_rect)
		self.all_sprites.draw(self.screen)
		self.screen.blit(self.icon, (8, HEIGHT - 132))
		self.draw_text(self.screen, self.update_text, 24, WIDTH - 256, HEIGHT - 32, WHITE)
		self.draw_text(self.screen, "Current Wave: " + str(self.wave), 32, WIDTH - 164, 32, WHITE)
		self.draw_text(self.screen, "Personal Best: " + str(self.high), 32, WIDTH - 164, 64, WHITE)
		self.draw_enemies(self.screen, 152, HEIGHT - 132, self.mob_icon)
		self.draw_bar(self.screen, 136, HEIGHT - 70, self.player.hp, 100, RED)
		self.draw_bar(self.screen, 136, HEIGHT - 38, self.player.amr, self.maxamr, GREY)
		pygame.display.flip()

	def show_start_screen(self):
		"""Creates a start up splash screen"""
		self.screen.blit(self.map_img, self.map_rect)
		self.draw_text(self.screen, "Press enter to begin!", 36, 648, 512, BLACK)
		self.screen.blit(self.logo, (240, 64))
		pygame.mixer.music.load(os.path.join(path.dirname(__file__), "snd", "menu.ogg"))
		pygame.mixer.music.play(loops = -1)
		pygame.display.flip()
		self.waiting = True
		while self.waiting:
			self.clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_ESCAPE:
						exit()
					if event.key != pygame.K_ESCAPE and event.key != pygame.K_RETURN:
						if event.key == pygame.K_r:
							self.cheater = []
							print("Code reset")
						if event.key != pygame.K_r:
							self.cheater.append(event.key)


					elif event.key == pygame.K_RETURN:
						pygame.mixer.music.load(os.path.join(path.dirname(__file__), "snd", "song1.wav"))
						pygame.mixer.music.play(loops = -1)
						if self.cheater == self.cheatcode:
							self.addmult = 10
							self.addamr = 1000
							print("YOU CHEATER")
							self.cheater = []
						if self.cheater == self.newgame:
							highscore.reset_high_score()
							print("Score Reset")
							self.cheater = []
						self.waiting = False
						self.running = True

	def show_go_screen(self):
		"""Creates a game over screen"""
		self.screen.blit(self.map_img, self.map_rect)
		self.draw_text(self.screen, "You made it to wave " + str(self.wave) + "!", 36, 648, 364, WHITE)
		self.draw_text(self.screen, "Your personal best is wave " + str(self.high) + "!", 36, 648, 412, WHITE)
		self.draw_text(self.screen, "Press enter to restart!", 36, 648, 512, WHITE)
		self.screen.blit(self.logo, (240, 64))
		pygame.display.flip()
		self.waiting = True
		while self.waiting:
			self.clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						exit()
					if event.key != pygame.K_ESCAPE and event.key != pygame.K_RETURN:
						if event.key == pygame.K_r:
							self.cheater = []
							print("Code reset")
						if event.key != pygame.K_r:
							self.cheater.append(event.key)

					elif event.key == pygame.K_RETURN:
						if self.cheater == self.cheatcode:
							self.addmult = 10
							self.amr = 1000
							self.cheater = []
							print("YOU CHEATER")
						if self.cheater == self.newgame:
							highscore.reset_high_score()
							print("Score Reset")
							self.cheater = []
						self.wave = 0
						self.waiting = False

def main():
	g = Game()
	g.show_start_screen()
	while g.running:
		g.run()
		g.show_go_screen()

main()
