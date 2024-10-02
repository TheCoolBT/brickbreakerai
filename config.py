# config.py

# Screen dimensions
WIDTH = 600
HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)
REGULAR_COLOR = GREY  # Color for regular bricks

# Paddle settings
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 7

# Ball settings
BALL_RADIUS = 8

# Brick settings
BRICK_ROWS = 4
BRICK_COLUMNS = 10
BRICK_WIDTH = WIDTH // BRICK_COLUMNS
BRICK_HEIGHT = 20

# Difficulty scaling
INITIAL_DIFFICULTY = 1.0  # Base average durability
DIFFICULTY_INCREMENT = 0.2  # Incremental increase per wave

# Other
FPS = 60
