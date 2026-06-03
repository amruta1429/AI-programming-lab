# ==============================
# FLAPPY BIRD GAME - PYTHON
# Works in Spyder
# ==============================

import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen size
WIDTH = 500
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont("Arial", 40)
small_font = pygame.font.SysFont("Arial", 25)

# Bird
bird_x = 100
bird_y = 300
bird_radius = 20

bird_velocity = 0
gravity = 0.5
jump = -10

# Pipes
pipe_width = 80
pipe_gap = 180
pipe_speed = 5

pipes = []

# Score
score = 0
high_score = 0

# Game state
game_over = False


# Create pipe
def create_pipe():
    pipe_height = random.randint(150, 450)

    top_pipe = pygame.Rect(
        WIDTH,
        0,
        pipe_width,
        pipe_height
    )

    bottom_pipe = pygame.Rect(
        WIDTH,
        pipe_height + pipe_gap,
        pipe_width,
        HEIGHT
    )

    return (top_pipe, bottom_pipe)


# Reset game
def reset_game():
    global bird_y
    global bird_velocity
    global pipes
    global score
    global game_over

    bird_y = 300
    bird_velocity = 0
    pipes = []
    score = 0
    game_over = False

    pipes.append(create_pipe())


# First pipe
pipes.append(create_pipe())


# Main Loop
running = True

while running:

    clock.tick(FPS)

    # Background
    screen.fill(BLUE)

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                if game_over:
                    reset_game()

                else:
                    bird_velocity = jump

    # Game Logic
    if not game_over:

        # Bird movement
        bird_velocity += gravity
        bird_y += bird_velocity

        # Bird draw
        pygame.draw.circle(
            screen,
            YELLOW,
            (bird_x, int(bird_y)),
            bird_radius
        )

        # Move pipes
        for pipe_pair in pipes:

            pipe_pair[0].x -= pipe_speed
            pipe_pair[1].x -= pipe_speed

        # Remove old pipe
        if pipes[0][0].x < -pipe_width:

            pipes.pop(0)

            score += 1

            if score > high_score:
                high_score = score

        # Add new pipe
        if pipes[-1][0].x < 250:
            pipes.append(create_pipe())

        # Draw pipes
        for top_pipe, bottom_pipe in pipes:

            pygame.draw.rect(screen, GREEN, top_pipe)
            pygame.draw.rect(screen, GREEN, bottom_pipe)

            # Bird collision box
            bird_rect = pygame.Rect(
                bird_x - bird_radius,
                bird_y - bird_radius,
                bird_radius * 2,
                bird_radius * 2
            )

            # Collision
            if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
                game_over = True

        # Screen collision
        if bird_y < 0 or bird_y > HEIGHT:
            game_over = True

        # Score text
        score_text = font.render(
            "Score: " + str(score),
            True,
            WHITE
        )

        screen.blit(score_text, (20, 20))

        high_text = small_font.render(
            "High Score: " + str(high_score),
            True,
            WHITE
        )

        screen.blit(high_text, (20, 70))

    else:

        game_over_text = font.render(
            "GAME OVER",
            True,
            WHITE
        )

        restart_text = small_font.render(
            "Press SPACE to Restart",
            True,
            WHITE
        )

        screen.blit(game_over_text, (120, 300))
        screen.blit(restart_text, (110, 380))

    # Update screen
    pygame.display.update()

# Quit
pygame.quit()
sys.exit()