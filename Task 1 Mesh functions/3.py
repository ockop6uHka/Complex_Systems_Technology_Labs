import pygame
import numpy as np

pygame.init()
screen_width, screen_height = 1000, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Метод Эйлера для задач (a)-(d)")
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

h = 0.025
x_values = np.arange(0, 10 + h, h)


def to_screen_coords(x, y, x_min, x_max, y_min, y_max):
    scale_x = screen_width / (x_max - x_min)
    scale_y = screen_height / (y_max - y_min)
    screen_x = (x - x_min) * scale_x
    screen_y = screen_height - (y - y_min) * scale_y
    return int(screen_x), int(screen_y)


def draw_axes(x_min, x_max, y_min, y_max):
    pygame.draw.line(screen, (200, 200, 200), (0, screen_height // 2), (screen_width, screen_height // 2), 1)
    pygame.draw.line(screen, (200, 200, 200), (screen_width // 2, 0), (screen_width // 2, screen_height), 1)

    step_x = max(1, int((x_max - x_min) / 10))
    for x in range(int(x_min), int(x_max) + 1, step_x):
        screen_x, _ = to_screen_coords(x, 0, x_min, x_max, y_min, y_max)
        if 0 <= screen_x <= screen_width:
            label = font.render(str(x), True, (255, 255, 255))
            screen.blit(label, (screen_x - 10, screen_height // 2 + 5))

    step_y = max(1, int((y_max - y_min) / 10))
    for y in range(int(y_min), int(y_max) + 1, step_y):
        _, screen_y = to_screen_coords(0, y, x_min, x_max, y_min, y_max)
        if 0 <= screen_y <= screen_height:
            label = font.render(str(y), True, (255, 255, 255))
            screen.blit(label, (screen_width // 2 + 5, screen_y - 10))


problems = []


def f_a(y):
    return 0.5 * y


def euler_a():
    y = np.zeros(len(x_values))
    y[0] = 1
    for i in range(1, len(x_values)):
        y[i] = y[i - 1] + h * f_a(y[i - 1])
    return y


problems.append(("Задача (a): y' = 1/2 y, y(0) = 1", lambda: (x_values, euler_a())))


def f_b(x, y):
    return 2 * x + 3 * y


def euler_b():
    y = np.zeros(len(x_values))
    y[0] = -2
    for i in range(1, len(x_values)):
        y[i] = y[i - 1] + h * f_b(x_values[i - 1], y[i - 1])
    return y


problems.append(("Задача (b): y' = 2x + 3y, y(0) = -2", lambda: (x_values, euler_b())))


def f_c1(x2):
    return x2


def f_c2(x1):
    return -x1


def euler_c():
    x1 = np.zeros(len(x_values))
    x2 = np.zeros(len(x_values))
    x1[0], x2[0] = 1, 0
    for i in range(1, len(x_values)):
        x1[i] = x1[i - 1] + h * f_c1(x2[i - 1])
        x2[i] = x2[i - 1] + h * f_c2(x1[i - 1])
    return x1, x2


problems.append(("Задача (c): x1' = x2, x2' = -x1", lambda: (x_values, *euler_c())))

running = True
current_problem = 0
animation_progress = 0
animation_speed = 10

while running:
    screen.fill((30, 30, 30))
    title, data_func = problems[current_problem]
    result = data_func()
    x, *y_values = result

    x_min, x_max = x[0], x[-1]
    y_min, y_max = min(map(np.min, y_values)), max(map(np.max, y_values))

    draw_axes(x_min, x_max, y_min, y_max)

    for y in y_values:
        for i in range(min(animation_progress, len(x))):
            x_screen, y_screen = to_screen_coords(x[i], y[i], x_min, x_max, y_min, y_max)
            pygame.draw.circle(screen, (0, 255, 0), (x_screen, y_screen), 2)

    animation_progress += animation_speed
    if animation_progress > len(x):
        animation_progress = len(x)

    title_surface = font.render(title, True, (255, 255, 255))
    screen.blit(title_surface, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                current_problem = (current_problem + 1) % len(problems)
                animation_progress = 0
            elif event.key == pygame.K_LEFT:
                current_problem = (current_problem - 1) % len(problems)
                animation_progress = 0

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
