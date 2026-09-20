import pygame

from src.obstacle import Obstacle
from src.player import Player
from src.settings import (
    FLY_ANIMATION_EVENT,
    FPS,
    FONT_PATH,
    GROUND_IMAGE,
    OBSTACLE_SPAWN_EVENT,
    OBSTACLE_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SKY_IMAGE,
)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Runner game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(str(FONT_PATH), 50)

        self.sky_surface = pygame.image.load(str(SKY_IMAGE)).convert()
        self.ground_surface = pygame.image.load(str(GROUND_IMAGE)).convert()
        self.player = Player()
        self.obstacles = []

        self.game_active = False
        self.running = True
        self.start_time = 0
        self.score = 0

        self.player_stand_rectangle = self.player.stand_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.game_name = self.font.render(
            "Runner game", False, (111, 196, 169))
        self.game_name_rectangle = self.game_name.get_rect(
            center=(SCREEN_WIDTH // 2, 80))
        self.game_message = self.font.render(
            "Press space to run", False, (111, 196, 169))
        self.game_message_rectangle = self.game_message.get_rect(
            center=(SCREEN_WIDTH // 2, 340))

        pygame.time.set_timer(OBSTACLE_SPAWN_EVENT, 1500)

    def start_game(self):
        self.game_active = True
        self.start_time = int(pygame.time.get_ticks() / 100)
        self.score = 0
        self.obstacles.clear()
        self.player.reset()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return

        if self.game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.player.rect.collidepoint(event.pos):
                    self.player.jump()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player.jump()
            elif event.type == OBSTACLE_SPAWN_EVENT:
                self.obstacles.append(Obstacle.create_random())
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.start_game()

    def update(self):
        if not self.game_active:
            return

        self.player.update()
        for obstacle in self.obstacles:
            obstacle.update(OBSTACLE_SPEED)
        self.obstacles = Obstacle.remove_off_screen(self.obstacles)

        if any(self.player.rect.colliderect(obstacle.rect)
               for obstacle in self.obstacles):
            self.game_active = False

        self.score = int(pygame.time.get_ticks() / 100) - self.start_time

    def draw(self):
        if self.game_active:
            self.screen.blit(self.sky_surface, (0, 0))
            self.screen.blit(self.ground_surface, (0, 300))
            score_surface = self.font.render(
                f"Score: {self.score}", False, (64, 64, 64))
            score_rectangle = score_surface.get_rect(center=(400, 50))
            self.screen.blit(score_surface, score_rectangle)

            self.player.draw(self.screen)
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)
            return

        self.screen.fill((94, 129, 162))
        self.screen.blit(self.player.stand_surface,
                         self.player_stand_rectangle)
        self.screen.blit(self.game_name, self.game_name_rectangle)

        if self.score == 0:
            self.screen.blit(self.game_message, self.game_message_rectangle)
        else:
            score_message = self.font.render(
                f"Your score: {self.score}", False, (111, 196, 169))
            score_rectangle = score_message.get_rect(center=(400, 330))
            self.screen.blit(score_message, score_rectangle)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()
