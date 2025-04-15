import pygame
import sys
import random

# Initialize
pygame.init()
WIDTH, HEIGHT = 640, 480
TILE_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake Adventure")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

font = pygame.font.SysFont(None, 36)

# Snake and Game Data
snake = [(5, 5)]
direction = (1, 0)
food = (10, 10)
power_up = None
obstacles = []
score = 0
level = 1
speed = 10
food_eaten = 0

def draw_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def spawn_food():
    while True:
        new_food = (random.randint(0, WIDTH // TILE_SIZE - 1), random.randint(0, HEIGHT // TILE_SIZE - 1))
        if new_food not in snake and new_food not in obstacles:
            return new_food

def spawn_power_up():
    if random.random() < 0.2:
        while True:
            pu = (random.randint(0, WIDTH // TILE_SIZE - 1), random.randint(0, HEIGHT // TILE_SIZE - 1))
            if pu not in snake and pu != food and pu not in obstacles:
                return pu
    return None

def spawn_obstacles(count):
    obs = []
    while len(obs) < count:
        o = (random.randint(0, WIDTH // TILE_SIZE - 1), random.randint(0, HEIGHT // TILE_SIZE - 1))
        if o not in snake and o != food and o not in obs:
            obs.append(o)
    return obs

def reset_game():
    global snake, direction, food, power_up, obstacles, score, level, speed, food_eaten
    snake = [(5, 5)]
    direction = (1, 0)
    food = spawn_food()
    power_up = None
    obstacles = spawn_obstacles(level + 2)
    score = 0
    level = 1
    speed = 10
    food_eaten = 0

reset_game()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != (0, 1):
        direction = (0, -1)
    elif keys[pygame.K_DOWN] and direction != (0, -1):
        direction = (0, 1)
    elif keys[pygame.K_LEFT] and direction != (1, 0):
        direction = (-1, 0)
    elif keys[pygame.K_RIGHT] and direction != (-1, 0):
        direction = (1, 0)

    # Move Snake
    head_x, head_y = snake[0]
    new_head = ((head_x + direction[0]) % (WIDTH // TILE_SIZE), 
                (head_y + direction[1]) % (HEIGHT // TILE_SIZE))

    if new_head in snake or new_head in obstacles:
        reset_game()
        continue

    snake.insert(0, new_head)

    # Food collision
    if new_head == food:
        score += 10
        food = spawn_food()
        food_eaten += 1
        if food_eaten % 5 == 0:
            level += 1
            speed += 2
            obstacles.extend(spawn_obstacles(2))
        power_up = spawn_power_up()
    else:
        snake.pop()

    # Power-up collision
    if power_up and new_head == power_up:
        score += 30
        power_up = None

    # Draw
    screen.fill((0, 0, 0))

    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0]*TILE_SIZE, segment[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw food
    pygame.draw.rect(screen, RED, (food[0]*TILE_SIZE, food[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw power-up
    if power_up:
        pygame.draw.rect(screen, BLUE, (power_up[0]*TILE_SIZE, power_up[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, GRAY, (obs[0]*TILE_SIZE, obs[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw HUD
    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"Level: {level}", 10, 40)

    pygame.display.flip()
    clock.tick(speed)
