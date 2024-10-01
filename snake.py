import pygame
import time
import random
import math

pygame.init()
pygame.mixer.init()

RED = (213, 50, 80)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
SKYBLUE = (135, 206, 235)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 0)
GREY = (169, 169, 169)

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game with Obstacles')

clock = pygame.time.Clock()
SNAKE_BLOCK = 10
SNAKE_SPEED = 10

snake_image = pygame.image.load('snake.png')
snake_image = pygame.transform.scale(snake_image, (SNAKE_BLOCK, SNAKE_BLOCK))

eat_sound = pygame.mixer.Sound('eat.mp3')
game_over_sound = pygame.mixer.Sound('game_over.wav')
pygame.mixer.music.load('background.mp3')

pygame.mixer.music.play(-1)

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def show_score(score):
    value = score_font.render("Your Score: " + str(score), True, BLACK)
    screen.blit(value, [0, 0])

def draw_snake(snake_segments):
    for segment in snake_segments:
        screen.blit(snake_image, (segment[0], segment[1]))

def show_message(msg, color):
    message = font_style.render(msg, True, color)
    screen.blit(message, [WIDTH / 6, HEIGHT / 3])

def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(screen, RED, [obs[0], obs[1], SNAKE_BLOCK, SNAKE_BLOCK])

def draw_gradient_background(start_color, end_color):
    for y in range(HEIGHT):
        color = (
            int(start_color[0] + (end_color[0] - start_color[0]) * y / HEIGHT),
            int(start_color[1] + (end_color[1] - start_color[1]) * y / HEIGHT),
            int(start_color[2] + (end_color[2] - start_color[2]) * y / HEIGHT)
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

def animate_food(food_x, food_y, frame):
    size = SNAKE_BLOCK // 2 + int(5 * (1 + math.sin(frame / 5)))
    pygame.draw.circle(screen, ORANGE, (int(food_x + SNAKE_BLOCK // 2), int(food_y + SNAKE_BLOCK // 2)), size)

def game_over_animation(snake_segments):
    for i in range(len(snake_segments), 0, -1):
        del snake_segments[0]
        screen.fill(BLUE)
        draw_snake(snake_segments)
        pygame.display.update()
        time.sleep(0.05)

def game_loop():
    game_over = False
    game_close = False
    x = WIDTH / 2
    y = HEIGHT / 2
    x_change = 0
    y_change = 0
    direction = 'RIGHT'
    next_direction = 'RIGHT'
    snake_segments = [[100, 50]]
    snake_length = 1
    food_x = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    food_y = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
    frame = 0

    obstacles = []
    for _ in range(15):
        obs_x = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
        obs_y = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
        obstacles.append([obs_x, obs_y])

    center_width_start = WIDTH // 3
    center_width_end = 2 * WIDTH // 3
    center_height_start = HEIGHT // 3
    center_height_end = 2 * HEIGHT // 3

    for _ in range(5):
        obs_x = round(random.randrange(center_width_start, center_width_end - SNAKE_BLOCK) / 10.0) * 10.0
        obs_y = round(random.randrange(center_height_start, center_height_end - SNAKE_BLOCK) / 10.0) * 10.0
        obstacles.append([obs_x, obs_y])

    while not game_over:
        while game_close:
            pygame.mixer.music.stop()
            if not pygame.mixer.get_busy():
                game_over_sound.play()
            screen.fill(BLUE)
            show_message("23CS3048 \n Game Over! Press E to Exit or R to Restart", RED)
            show_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        game_over_sound.stop()
                        pygame.mixer.music.play(-1)
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != 'RIGHT':
                    next_direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    next_direction = 'RIGHT'
                elif event.key == pygame.K_UP and direction != 'DOWN':
                    next_direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    next_direction = 'DOWN'

        direction = next_direction

        if direction == 'LEFT':
            x_change = -SNAKE_BLOCK
            y_change = 0
        elif direction == 'RIGHT':
            x_change = SNAKE_BLOCK
            y_change = 0
        elif direction == 'UP':
            y_change = -SNAKE_BLOCK
            x_change = 0
        elif direction == 'DOWN':
            y_change = SNAKE_BLOCK
            x_change = 0

        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        x += x_change
        y += y_change
        draw_gradient_background(SKYBLUE, GREY)

        animate_food(food_x, food_y, frame)
        frame += 1

        draw_obstacles(obstacles)

        snake_head = [x, y]
        snake_segments.append(snake_head)
        if len(snake_segments) > snake_length:
            del snake_segments[0]

        for segment in snake_segments[:-1]:
            if segment == snake_head:
                game_close = True

        for obs in obstacles:
            if x == obs[0] and y == obs[1]:
                game_close = True

        draw_snake(snake_segments)
        show_score(snake_length - 1)
        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            food_y = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            snake_length += 1
            eat_sound.play()

        clock.tick(SNAKE_SPEED)

    game_over_animation(snake_segments)
    pygame.quit()
    quit()

game_loop()
