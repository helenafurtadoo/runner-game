import pygame
from random import randint

from src.settings import (
    FLY_1,
    FLY_2,
    FONT_PATH,
    GROUND_IMAGE,
    OBSTACLE_SPAWN_EVENT,
    PLAYER_JUMP,
    PLAYER_STAND,
    PLAYER_WALK_1,
    PLAYER_WALK_2,
    SKY_IMAGE,
    SNAIL_1,
    SNAIL_2,
)


def display_score():
    current_time = int(pygame.time.get_ticks() / 100) - start_time
    score_surface = test_font.render(
        f'Score: {current_time}', False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rectangle)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)
        # list compreshion --> limpeza de memoria e gestao de obstaculo
        # so add um obstaculo na lista, se x > -100 ||| # atualize minha lista de obstcls, matendo apenas aqueles que ainda nao sairam da tela pela esquerda (x > 0)
        obstacle_list = [
            obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def player_animation():
    # mostrar a animacao andando, se o player estiver no chao E mostrar a animacao jump, se o player nao estiver no chao
    global player_surface, player_index

    if player_rectangle.bottom < 300:
        # jump animation
        player_surface = player_jump
    else:
        # walk animation (alternar entre walk1 e walk2, por isso usar o index)
        player_index += 0.1
        # quando o index chegar a 1, dps de ir polando de 0.1, quero que volte a zero, pq a lista tem apenas 2 elementos, 0 e 1(walk1 | walk2)
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]


pygame.init()

# ===== DISPLAY SURFACE ====
# criando display surfice (janela de exibição)
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner game")  # criando o nome do display surfice
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0

# ==== FONTE =====
test_font = pygame.font.Font(str(FONT_PATH), 50)

# REGULAR SURFICES
sky_surface = pygame.image.load(str(SKY_IMAGE)).convert()
ground_surface = pygame.image.load(str(GROUND_IMAGE)).convert()


# ==== OBSTACULOS ====
# SNAIL SURFACE
snail_frame_1 = pygame.image.load(str(SNAIL_1)).convert_alpha()
snail_frame_2 = pygame.image.load(str(SNAIL_2)).convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]
# FLYER SURFACE
fly_frame_1 = pygame.image.load(str(FLY_1)).convert_alpha()
fly_frame_2 = pygame.image.load(str(FLY_2)).convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

# PLAYER SURFACE
player_walk_1 = pygame.image.load(str(PLAYER_WALK_1)).convert_alpha()
player_walk_2 = pygame.image.load(str(PLAYER_WALK_2)).convert_alpha()
player_walk = [player_walk_1, player_walk_2]  # para fazer animacao grafica
player_index = 0
player_jump = pygame.image.load(str(PLAYER_JUMP)).convert_alpha()

player_surface = player_walk[player_index]
player_rectangle = player_surface.get_rect(midbottom=(80, 300))
# PLAYER GRAVITY
player_gravity = 0


# ==== INTRO SCREEN ====
player_stand = pygame.image.load(str(PLAYER_STAND)).convert_alpha()
# 2.pegando a imagem, e a transformando com pygame.transoform.rotozoom(faz uma rotacao da imagem)
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
# 3.criando o retangulo em volta da imagem player
player_stand_rectangle = player_stand.get_rect(center=(400, 200))

game_name = test_font.render('Runner game', False, (111, 196, 169))
game_name_rectangle = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press space to run',  False, (111, 196, 169))
game_message_rectangle = game_message.get_rect(center=(400, 340))

# ===== TIMER =====
obstacle_timer = OBSTACLE_SPAWN_EVENT
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

running = True
while running:
    for event in pygame.event.get():
        # CHECANDO O DISPLAY SURFICE PARA PODER FECHAR
        if event.type == pygame.QUIT:
            running = False

        if game_active:
            # CHECANDO MOVIMENTOS DO MOUSE
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rectangle.collidepoint(event.pos) and player_rectangle.bottom >= 300:
                    player_gravity = -20

            # CHECANDO INPUT KEYBOARD
            if event.type == pygame.KEYDOWN:
                # aqui o player so pode pular dnv, quando estiver tocando no chao. Para evitar pular muito, e sair da tela
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300:
                    player_gravity = -20
        else:  # caso seja game over, aperta espaco para voltar ao inicio
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

                start_time = int(pygame.time.get_ticks() / 100)

        # temporizador para spawn o inimigo
        if game_active:
            if event.type == obstacle_timer and game_active:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surf.get_rect(
                        bottomright=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surf .get_rect(
                        bottomright=(randint(900, 1100), 210)))

            # mudar a snail, para a animacao
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
            # mudar o fly, para a animacao
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

    if game_active:
        # PRINTING THE SURFACES
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        # pygame.draw.rect(screen, '#c0e8ec', score_rectangle,border_radius = 10)
        # screen.blit(score_surface, score_rectangle)
        score = display_score()

        # snail_rectangle.x-= 4
        # if snail_rectangle.right <= 0: snail_rectangle.left = 800 # se a parte direita retangulo da lesma for <= 0 (), "renascer" a lesma no 800 (mais esquerda possivel do x)
        # screen.blit(snail_surface, snail_rectangle)

        # ==== PLAYER ====
        player_gravity += 1
        player_rectangle.y += player_gravity
        if player_rectangle.bottom >= 300:
            # se o player estiver em um ponto >= 300, colocar ele de volta no 300 (pos y) | BARREIRA PARA MANTES O PLAYER NA ALTURA DO CHAO
            player_rectangle.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rectangle)

        # ==== MOVIMENTOS DO OBSTACULO =====
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # ==== COLISAO ====
        game_active = collisions(player_rectangle, obstacle_rect_list)

        # display_score()
    else:
        screen.fill((94, 129, 162))
        # desenhando passos 1,2,3 do PLAYER
        screen.blit(player_stand, player_stand_rectangle)
        obstacle_rect_list.clear()
        player_rectangle.midbottom = (80, 300)
        player_gravity = 0

        score_message = test_font.render(
            f'Your score: {score}', False, (111, 196, 169))
        score_message_rectangle = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rectangle)

        # se n tem score, pede para apertar espaço para comecar. Se tem score, mostra o score
        if score == 0:
            screen.blit(game_message, game_message_rectangle)
        else:
            screen.blit(score_message, score_message_rectangle)

    # ==== ATUALIZANDO TUDO =====
    pygame.display.update()
    clock.tick(60)
