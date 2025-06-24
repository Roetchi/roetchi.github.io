import pygame
import random

pygame.init()

BLOCK_SIZE = 20
WIDTH, HEIGHT = 500, 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game by Ömer Efe Özçelik")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
GRID_COLOR = (100, 180, 255)

font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 18)

def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, (*segment, BLOCK_SIZE, BLOCK_SIZE))

def draw_food(food_positions):
    for food in food_positions:
        pygame.draw.rect(screen, RED, (*food, BLOCK_SIZE, BLOCK_SIZE))

def draw_score(score, speed):
    text = font.render(f"Score: {score} Speed: {speed}", True, WHITE)
    screen.blit(text, (10, 10))

def draw_pause_hint():
    hint = small_font.render("P = Pause", True, WHITE)
    screen.blit(hint, (WIDTH - 110, 10))

def show_message(text, color, y_offset=0, small=False):
    f = small_font if small else font
    rendered = f.render(text, True, color)
    rect = rendered.get_rect(center=(WIDTH//2, HEIGHT//2 + y_offset))
    screen.blit(rendered, rect)

def spawn_food(snake_body, current_food):
    while True:
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        pos = (x, y)
        if pos not in snake_body and pos not in current_food:
            return pos

def title_screen():
    while True:
        screen.fill(BLUE)
        show_message("Welcome to Snake Game", WHITE, -30)
        show_message("Press ENTER to Play or Q to Quit", WHITE, 20, small=True)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def pause_screen():
    screen.fill(BLUE)
    show_message("PAUSED", WHITE, -60)
    show_message("W / ↑ = Up", WHITE, 20, small=True)
    show_message("S / ↓ = Down", WHITE, 45, small=True)
    show_message("A / ← = Left", WHITE, 70, small=True)
    show_message("D / → = Right", WHITE, 95, small=True)
    show_message("P = Pause / Resume", WHITE, 120, small=True)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                return

def game_loop():
    title_screen()
    x, y = WIDTH // 2, HEIGHT // 2
    x = (x // BLOCK_SIZE) * BLOCK_SIZE
    y = (y // BLOCK_SIZE) * BLOCK_SIZE
    direction = (BLOCK_SIZE, 0)
    snake = [(x, y)]
    snake_length = 1
    max_food = 3
    food_positions = [spawn_food(snake, [])]
    score = 0
    speed = 5
    max_speed = 10
    foods_eaten = 0
    running = True

    while running:
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                dx, dy = direction
                if event.key in [pygame.K_LEFT, pygame.K_a] and dx == 0:
                    direction = (-BLOCK_SIZE, 0)
                elif event.key in [pygame.K_RIGHT, pygame.K_d] and dx == 0:
                    direction = (BLOCK_SIZE, 0)
                elif event.key in [pygame.K_UP, pygame.K_w] and dy == 0:
                    direction = (0, -BLOCK_SIZE)
                elif event.key in [pygame.K_DOWN, pygame.K_s] and dy == 0:
                    direction = (0, BLOCK_SIZE)
                elif event.key == pygame.K_p:
                    pause_screen()

        if not running:
            break

        x += direction[0]
        y += direction[1]
        new_head = (x, y)

        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or new_head in snake:
            break

        snake.append(new_head)
        if len(snake) > snake_length:
            snake.pop(0)

        if new_head in food_positions:
            food_positions.remove(new_head)
            snake_length += 1
            score += 1
            foods_eaten += 1
            if len(food_positions) < max_food:
                food_positions.append(spawn_food(snake, food_positions))
            if foods_eaten % 5 == 0 and speed < max_speed:
                speed += 1

        screen.fill(BLUE)
        draw_grid()
        draw_snake(snake)
        draw_food(food_positions)
        draw_score(score, speed)
        draw_pause_hint()
        pygame.display.flip()

    screen.fill(BLUE)
    show_message("Game Over!", RED, -20)
    show_message("Press R to Restart or Q to Quit", WHITE, 30, small=True)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_r:
                    game_loop()

game_loop()
pygame.quit()
