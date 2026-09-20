from pathlib import Path

import pygame


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"

FONT_PATH = ASSETS_DIR / "fonts" / "Pixeltype.ttf"
BACKGROUND_DIR = ASSETS_DIR / "backgrounds" / "grafico"
PLAYER_DIR = BACKGROUND_DIR / "player"
SNAIL_DIR = BACKGROUND_DIR / "snail"
FLY_DIR = BACKGROUND_DIR / "fly"

SKY_IMAGE = BACKGROUND_DIR / "ceu.png"
GROUND_IMAGE = BACKGROUND_DIR / "chao.png"

PLAYER_WALK_1 = PLAYER_DIR / "player_walk_1.png"
PLAYER_WALK_2 = PLAYER_DIR / "player_walk_2.png"
PLAYER_JUMP = PLAYER_DIR / "jump.png"
PLAYER_STAND = PLAYER_DIR / "player_stand.png"

SNAIL_1 = SNAIL_DIR / "snail1.png"
SNAIL_2 = SNAIL_DIR / "snail2.png"

FLY_1 = FLY_DIR / "Fly1.png"
FLY_2 = FLY_DIR / "Fly2.png"

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60

GROUND_Y = 300
PLAYER_START_POSITION = (80, GROUND_Y)

PLAYER_GRAVITY = 1
PLAYER_JUMP_FORCE = -20
OBSTACLE_SPEED = 5

OBSTACLE_SPAWN_EVENT = pygame.USEREVENT + 1
SNAIL_ANIMATION_EVENT = pygame.USEREVENT + 2
FLY_ANIMATION_EVENT = pygame.USEREVENT + 3