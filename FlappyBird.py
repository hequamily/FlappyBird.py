import pygame
import random

# Game settings
WIDTH = 400
HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = 5
GRAVITY = 0.5

# Pipe settings
PIPE_WIDTH = 70
PIPE_HEIGHT = random.randint(150, 400)
PIPE_GAP = 200
PIPE_SPEED = 3

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def new_pipe():
    p = {"x": WIDTH, "y": random.randint(150, 400)}
    return p


def draw_pipe(p):
    pygame.draw.rect(screen, WHITE, (p["x"], 0, PIPE_WIDTH, p["y"]))
    pygame.draw.rect(screen, WHITE, (p["x"], p["y"] + PIPE_GAP, PIPE_WIDTH, HEIGHT - p["y"] - PIPE_GAP))


def player_collide(p):
    if player_rect.colliderect(pygame.Rect(p["x"], 0, PIPE_WIDTH, p["y"])) or \
            player_rect.colliderect(pygame.Rect(p["x"], p["y"] + PIPE_GAP, PIPE_WIDTH, HEIGHT - p["y"] - PIPE_GAP)):
        return True
    return False


player_rect = pygame.Rect(50, HEIGHT / 2 - PLAYER_HEIGHT / 2, PLAYER_WIDTH, PLAYER_HEIGHT)
player_speed = 0
score = 0
game_over = False
pipes = [new_pipe()]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player_speed = -10
            elif event.key == pygame.K_SPACE and game_over:
                game_over = False
                player_rect = pygame.Rect(50, HEIGHT / 2 - PLAYER_HEIGHT / 2, PLAYER_WIDTH, PLAYER_HEIGHT)
                pipes = [new_pipe()]
                score = 0

    if not game_over:
        # Update player
        player_speed += GRAVITY
        player_rect.y += player_speed

        # Update pipes
        for p in pipes:
            p["x"] -= PIPE_SPEED

            if p["x"] + PIPE_WIDTH < 0:
                pipes.remove(p)
                score += 1

            if player_collide(p):
                game_over = True

        # Generate new pipe
        if pipes[-1]["x"] + PIPE_WIDTH < WIDTH - PIPE_GAP:
            pipes.append(new_pipe())

    screen.fill(BLACK)

    # Draw player
    pygame.draw.rect(screen, WHITE, player_rect)

    # Draw pipes
    for p in pipes:
        draw_pipe(p)

    # Draw score
    draw_text(screen, str(score), 18, WIDTH / 2, 10)

    if game_over:
        draw_text(screen, "Game Over", 30, WIDTH / 2, HEIGHT / 2)
        draw_text(screen, f"Score: {score}", 20, WIDTH / 2, HEIGHT / 2 + 30)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()






