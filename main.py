import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Paddle settings
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 7
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 20, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball settings
BALL_RADIUS = 8
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, BALL_RADIUS)
ball_speed_x = 3 * random.choice((1, -1))
ball_speed_y = 3 * random.choice((1, -1))

# Brick settings
BRICK_ROWS = 5
BRICK_COLUMNS = 10
BRICK_WIDTH = WIDTH // BRICK_COLUMNS
BRICK_HEIGHT = 20
bricks = [pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
          for row in range(BRICK_ROWS) for col in range(BRICK_COLUMNS)]

# Game variables
clock = pygame.time.Clock()
score = 0
font = pygame.font.Font(None, 36)

# Functions
def draw_objects():
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, RED, ball)

    for brick in bricks:
        pygame.draw.rect(screen, GREEN, brick)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def move_paddle():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += PADDLE_SPEED

def move_ball():
    global ball_speed_x, ball_speed_y, score
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with walls
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x *= -1
    if ball.top <= 0:
        ball_speed_y *= -1
    if ball.bottom >= HEIGHT:
        pygame.quit()
        sys.exit()

    # Ball collision with paddle
    if ball.colliderect(paddle):
        ball_speed_y *= -1

    # Ball collision with bricks
    hit_index = ball.collidelist(bricks)
    if hit_index != -1:
        brick = bricks.pop(hit_index)
        ball_speed_y *= -1
        score += 10

# Main game loop
running = True
while running:
    clock.tick(60)  # 60 frames per second
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    move_paddle()
    move_ball()
    draw_objects()

    pygame.display.flip()

pygame.quit()
