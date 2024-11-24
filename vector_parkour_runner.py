import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman Parkour Runner")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)

# Game variables
scroll_speed = 5
runner_x, runner_y = WIDTH // 5, HEIGHT - 150
runner_width, runner_height = 50, 80
gravity = 1
jump_height = -15
velocity_y = 0
ground_y = HEIGHT - 100
score = 0
game_over = False

# Obstacles and coins
obstacles = []
coins = []  # Define coins list
coin_image = pygame.Surface((30, 30))  # Replace with simple rectangle for coins
coin_image.fill(YELLOW)
coin_spawn_time = 0
obstacle_spawn_time = 0

# Runner hitbox
runner_rect = pygame.Rect(runner_x, runner_y, runner_width, runner_height)


def spawn_obstacle():
    """Spawns a new obstacle."""
    x = WIDTH
    y = ground_y - 40  # Smaller obstacle size
    obstacles.append(pygame.Rect(x, y, 40, 40))  # Smaller obstacle size


def spawn_coin():
    """Spawns a new coin."""
    x = WIDTH
    y = random.randint(ground_y - 200, ground_y - 50)
    return pygame.Rect(x, y, coin_image.get_width(), coin_image.get_height())


def draw_game():
    """Draws all game elements on the screen."""
    screen.fill(WHITE)

    # Draw ground
    pygame.draw.rect(screen, GREEN, (0, ground_y, WIDTH, HEIGHT - ground_y))

    # Draw stickman (player)
    # Head
    pygame.draw.circle(screen, BLACK, (runner_x + runner_width // 2, runner_y + 10), 10)
    # Body
    pygame.draw.line(screen, BLACK, (runner_x + runner_width // 2, runner_y + 20),
                     (runner_x + runner_width // 2, runner_y + 50), 3)
    # Arms
    pygame.draw.line(screen, BLACK, (runner_x + runner_width // 2 - 20, runner_y + 30),
                     (runner_x + runner_width // 2 + 20, runner_y + 30), 3)
    # Legs
    pygame.draw.line(screen, BLACK, (runner_x + runner_width // 2, runner_y + 50),
                     (runner_x + runner_width // 2 - 20, runner_y + 70), 3)
    pygame.draw.line(screen, BLACK, (runner_x + runner_width // 2, runner_y + 50),
                     (runner_x + runner_width // 2 + 20, runner_y + 70), 3)

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

    # Draw coins
    for coin in coins:
        screen.blit(coin_image, (coin.x, coin.y))

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Game Over
    if game_over:
        over_text = font.render("Game Over! Press R to Restart", True, RED)
        screen.blit(over_text, (WIDTH // 4, HEIGHT // 2))


# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                # Restart the game
                game_over = False
                runner_y = HEIGHT - 150
                velocity_y = 0
                obstacles.clear()
                coins.clear()
                score = 0

    # Check for input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and runner_y == ground_y - runner_height:
        velocity_y = jump_height

    # Apply gravity
    velocity_y += gravity
    runner_y += velocity_y

    # Prevent falling below the ground
    if runner_y >= ground_y - runner_height:
        runner_y = ground_y - runner_height

    # Update runner hitbox
    runner_rect.topleft = (runner_x, runner_y)

    # Spawn obstacles and coins
    obstacle_spawn_time += 1
    coin_spawn_time += 1

    if obstacle_spawn_time > 90:  # Adjust spawn frequency
        spawn_obstacle()
        obstacle_spawn_time = 0

    if coin_spawn_time > 120:  # Adjust spawn frequency
        coins.append(spawn_coin())
        coin_spawn_time = 0

    # Move obstacles
    for obstacle in obstacles[:]:
        obstacle.x -= scroll_speed
        if obstacle.x + obstacle.width < 0:
            obstacles.remove(obstacle)

    # Move coins
    for coin in coins[:]:
        coin.x -= scroll_speed
        if coin.x + coin.width < 0:
            coins.remove(coin)

    # Check for collisions with obstacles
    for obstacle in obstacles:
        if runner_rect.colliderect(obstacle):
            game_over = True

    # Check for collisions with coins
    for coin in coins[:]:
        if runner_rect.colliderect(coin):
            score += 10
            coins.remove(coin)

    # Draw everything
    draw_game()

    # Update display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)
