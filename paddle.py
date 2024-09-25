# paddle.py

import pygame
import random
from config import *

class Paddle:
    def __init__(self, color=None):
        self.rect = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 20, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = color if color is not None else random_color()

    def move_left(self):
        """Move the paddle to the left."""
        if self.rect.left > 0:  # Prevent the paddle from moving out of bounds
            self.rect.x -= PADDLE_SPEED

    def move_right(self):
        """Move the paddle to the right."""
        if self.rect.right < WIDTH:  # Prevent the paddle from moving out of bounds
            self.rect.x += PADDLE_SPEED

    def draw(self, screen):
        """Draw the paddle on the screen."""
        pygame.draw.rect(screen, self.color, self.rect)

def random_color():
    """Generates a random RGB color."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
