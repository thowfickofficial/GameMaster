import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
CAR_WIDTH, CAR_HEIGHT = 40, 80
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 50
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game")

# Load images
road_img = pygame.image.load("road.png")
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

car_img = pygame.image.load("car.png")
car_img = pygame.transform.scale(car_img, (CAR_WIDTH, CAR_HEIGHT))

obstacle_img = pygame.image.load("obstacle.png")
obstacle_img = pygame.transform.scale(obstacle_img, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

# Initialize car position
car_x = WIDTH // 2 - CAR_WIDTH // 2
car_y = HEIGHT - CAR_HEIGHT - 20

# Initialize obstacle
obstacle_x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
obstacle_y = 0
obstacle_speed = 5

# Game loop
running = True
score = 0
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > 0:
        car_x -= 5
    if keys[pygame.K_RIGHT] and car_x < WIDTH - CAR_WIDTH:
        car_x += 5

    # Move obstacle
    obstacle_y += obstacle_speed

    # Check collision
    if (
        car_x < obstacle_x + OBSTACLE_WIDTH
        and car_x + CAR_WIDTH > obstacle_x
        and car_y < obstacle_y + OBSTACLE_HEIGHT
        and car_y + CAR_HEIGHT > obstacle_y
    ):
        running = False

    # Spawn a new obstacle
    if obstacle_y > HEIGHT:
        obstacle_x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
        obstacle_y = 0
        score += 1

    # Clear the screen
    window.blit(road_img, (0, 0))

    # Draw car and obstacle
    window.blit(car_img, (car_x, car_y))
    window.blit(obstacle_img, (obstacle_x, obstacle_y))

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    window.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
