# brick.py

import pygame
from config import *

class Brick:
    def __init__(self, x, y, durability):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.durability = durability
        self.color = REGULAR_COLOR  # All bricks are regular color now

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 24)
        text = font.render(str(self.durability), True, WHITE)
        screen.blit(text, (self.rect.x + BRICK_WIDTH // 2 - 6, self.rect.y + BRICK_HEIGHT // 4))

