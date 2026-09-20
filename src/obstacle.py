from random import randint

import pygame

from src.settings import (
	FLY_1,
	FLY_2,
	GROUND_Y,
	SNAIL_1,
	SNAIL_2,
)


class Obstacle:
	def __init__(self, kind, rect, frames):
		self.kind = kind
		self.rect = rect
		self.frames = frames
		self.frame_index = 0
		self.surface = self.frames[self.frame_index]

	@classmethod
	def create_random(cls):
		if randint(0, 2):
			frames = [
				pygame.image.load(str(SNAIL_1)).convert_alpha(),
				pygame.image.load(str(SNAIL_2)).convert_alpha(),
			]
			surface = frames[0]
			rect = surface.get_rect(
				bottomright=(randint(900, 1100), GROUND_Y))
			return cls("snail", rect, frames)

		frames = [
			pygame.image.load(str(FLY_1)).convert_alpha(),
			pygame.image.load(str(FLY_2)).convert_alpha(),
		]
		surface = frames[0]
		rect = surface.get_rect(
			bottomright=(randint(900, 1100), 210))
		return cls("fly", rect, frames)

	def update(self, speed):
		self.rect.x -= speed
		self.frame_index = (self.frame_index + 1) % len(self.frames)
		self.surface = self.frames[self.frame_index]

	def draw(self, screen):
		screen.blit(self.surface, self.rect)

	def is_off_screen(self):
		return self.rect.right < 0

	@staticmethod
	def remove_off_screen(obstacles):
		return [obstacle for obstacle in obstacles
				if not obstacle.is_off_screen()]