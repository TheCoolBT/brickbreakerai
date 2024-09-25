import pygame
import neat
import os
import random
from config import *
from game_ball import Ball
from brick import Brick
from paddle import Paddle

pygame.init()

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEAT AI Brick Breaker")
clock = pygame.time.Clock()

# Game variables
balls = []
bricks = []
wave = 1  # Track the current wave
generation = 0  # Track generations
font = pygame.font.Font(None, 36)  # Font for displaying text

def random_color():
    """Generate a random RGB color."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def eval_genomes(genomes, config):
    global wave, generation
    generation += 1

    nets = []
    paddles = []
    ge = []
    scores = []  # Track the score for each AI
    paddle_balls = []  # Store (ball, paddle) pairs for initial balls

    # Setup NEAT agents
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        
        # Generate a random color for the paddle and its balls
        paddle_color = random_color()
        paddle = Paddle(color=paddle_color)
        paddles.append(paddle)
        
        # Create the initial ball with the paddle's color
        ball = Ball(WIDTH // 2, HEIGHT // 2, color=paddle_color)
        paddle_balls.append((ball, paddle))  # Track the initial ball and its owner
        
        genome.fitness = 0
        ge.append(genome)
        scores.append(0)  # Initialize scores

    spawn_new_wave(bricks, wave)

    # Game loop
    while len(paddles) > 0:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Move AI-controlled paddles and their associated balls
        for x in range(len(paddles)):
            paddle = paddles[x]
            ball, owner_paddle = paddle_balls[x]  # Each paddle can only interact with its own ball

            ball.move()

            # Neural network inputs: ball x, ball y, ball velocity, paddle x
            output = nets[x].activate((ball.rect.x, ball.rect.y, ball.speed_x, paddle.rect.x))

            # AI decides whether to move paddle left, right, or hold still
            if output[0] > 0.66:  # Move right
                paddle.move_right()
            elif output[0] < 0.33:  # Move left
                paddle.move_left()
            else:  # Else hold still
                pass

            # Check for ball-paddle collision (only owner interacts with its own ball)
            ball.check_paddle_collision(paddle)

            # Check for ball-brick collision
            if ball.check_brick_collision(bricks, paddle_balls, paddle):
                scores[x] += 1  # Increment score when a brick is destroyed
                ge[x].fitness += 10  # Give a significant fitness boost for destroying a brick

            # Check if the ball is out of bounds
            if ball.rect.bottom >= HEIGHT:
                ge[x].fitness -= 10  # Penalize fitness for missing the ball
                
                # Remove the paddle and its associated ball
                paddles.pop(x)
                nets.pop(x)
                ge.pop(x)
                paddle_balls.pop(x)
                scores.pop(x)
                break  # Exit the loop early to avoid index errors

            else:
                ge[x].fitness += 0.1  # Reward for keeping the ball in play

                # Reward for alignment with the ball on the x-axis
                if abs(paddle.rect.centerx - ball.rect.centerx) < 10:  # Allow a tolerance of 10 pixels
                    ge[x].fitness += 0.1  # Reward for being aligned with the ball's x-coordinate

        # If all bricks are destroyed, spawn a new wave
        if len(bricks) == 0:
            wave += 1
            spawn_new_wave(bricks, wave)

            # Increment ball speed after every wave
            for ball, _ in paddle_balls:
                ball.speed_x *= 1.05  # Increase speed by 5%
                ball.speed_y *= 1.05

        # --- Drawing section ---
        screen.fill(BLACK)

        # Draw game objects (paddles, balls, bricks)
        for paddle in paddles:
            paddle.draw(screen)
        for ball, _ in paddle_balls:
            ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)

        # Display generation info and current scores
        generation_text = font.render(f"Generation: {generation}", True, WHITE)
        ai_count_text = font.render(f"AI Remaining: {len(paddles)}", True, WHITE)
        screen.blit(generation_text, (10, 10))
        screen.blit(ai_count_text, (10, 50))

        # Display the score for each AI
        for idx, score in enumerate(scores):
            score_text = font.render(f"AI {idx + 1} Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 100 + idx * 30))

        pygame.display.flip()  # Update the screen

# Spawn a new wave of bricks
def spawn_new_wave(bricks, wave):
    bricks.clear()
    avg_durability = INITIAL_DIFFICULTY + (wave - 1) * DIFFICULTY_INCREMENT
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLUMNS):
            if random.random() < 0.7:  # 70% chance to spawn a brick
                durability = max(1, int(random.gauss(avg_durability, 1)))
                bricks.append(Brick(col * BRICK_WIDTH, row * BRICK_HEIGHT, durability))

# Setup NEAT
def run_neat(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, 
                                config_file)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Evolve for 50 generations
    population.run(eval_genomes, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat-config.txt")
    run_neat(config_path)
