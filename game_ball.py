# game_ball.py

import pygame
import random
from config import *

class Ball:
    def __init__(self, x, y, speed_x=None, speed_y=None, color=RED):
        self.rect = pygame.Rect(x, y, BALL_RADIUS, BALL_RADIUS)
        self.color = color  # Assign the ball's color
        
        # Ensure horizontal velocity is never zero and is either left or right
        self.speed_x = speed_x if speed_x is not None else random.choice([-3, 3])
        
        # Ensure the ball always moves downward with a non-zero vertical velocity
        self.speed_y = speed_y if speed_y is not None else 3

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Collision with walls
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0:
            self.speed_y *= -1

    def check_paddle_collision(self, paddle):
        if self.rect.colliderect(paddle.rect):
            self.speed_y *= -1
            return True
        return False

    def check_brick_collision(self, bricks, balls, owner_paddle):
        hit_index = self.rect.collidelist([brick.rect for brick in bricks])
        if hit_index != -1:
            brick = bricks[hit_index]
            brick.durability -= 1

            if brick.durability == 0:  # Brick is destroyed
                bricks.pop(hit_index)  # Remove the destroyed brick

            # Reverse the ball's direction after hitting the brick
            self.speed_y *= -1

            # Ensure the ball's speed doesn't get stuck at zero after collision
            if self.speed_y == 0:
                self.speed_y = 3  # Force it to move downwards if it gets stuck
            if self.speed_x == 0:
                self.speed_x = random.choice([-3, 3])  # Force horizontal movement if it gets stuck

            return True

        return False

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)
