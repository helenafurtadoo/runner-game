import pygame

from src.settings import (
    GROUND_Y,
    PLAYER_GRAVITY,
    PLAYER_JUMP,
    PLAYER_JUMP_FORCE,
    PLAYER_START_POSITION,
    PLAYER_STAND,
    PLAYER_WALK_1,
    PLAYER_WALK_2,
)


class Player:
    def __init__(self):
        self.walk_frames = [
            pygame.image.load(str(PLAYER_WALK_1)).convert_alpha(),
            pygame.image.load(str(PLAYER_WALK_2)).convert_alpha(),
        ]
        self.jump_surface = pygame.image.load(
            str(PLAYER_JUMP)).convert_alpha()
        self.stand_surface = pygame.image.load(
            str(PLAYER_STAND)).convert_alpha()
        self.stand_surface = pygame.transform.rotozoom(
            self.stand_surface, 0, 2)

        self.surface = self.walk_frames[0]
        self.rect = self.surface.get_rect(
            midbottom=PLAYER_START_POSITION)
        self.gravity = 0
        self.animation_index = 0

    def jump(self):
        if self.rect.bottom >= GROUND_Y:
            self.gravity = PLAYER_JUMP_FORCE

    def update(self):
        self.gravity += PLAYER_GRAVITY
        self.rect.y += self.gravity

        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y

        self.animate()

    def animate(self):
        if self.rect.bottom < GROUND_Y:
            self.surface = self.jump_surface
            return

        self.animation_index += 0.1
        if self.animation_index >= len(self.walk_frames):
            self.animation_index = 0
        self.surface = self.walk_frames[int(self.animation_index)]

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def reset(self):
        self.rect.midbottom = PLAYER_START_POSITION
        self.gravity = 0
        self.animation_index = 0
        self.surface = self.walk_frames[0]
