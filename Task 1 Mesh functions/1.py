import pygame
import numpy as np
import math

pygame.init()
screen_width, screen_height = 1000, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Графики функций")
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

steps = [0.01, 0.005, 0.001]

intervals = {
    "e^(-x/2)": [0, np.pi / 2],
    "sin(3x)": [2, 10],
    "cos^2(5x)": [-3, 3],
    "sum(x^(2n)/(2n)!) (cosh(x))": [-3, 3]
}

def f1(x):
    return np.exp(-x / 2)

def f2(x):
    return np.sin(3 * x)

def f3(x):
    return np.cos(5 * x) ** 2

def f4(x):
    terms = [x ** (2 * n) / math.factorial(2 * n) for n in range(10)]
    return np.sum(terms, axis=0)

functions = {
    "e^(-x/2)": f1,
    "sin(3x)": f2,
    "cos^2(5x)": f3,
    "sum(x^(2n)/(2n)!) (cosh(x))": f4
}

def to_screen_coords(x, y, x_min, x_max, y_min, y_max):
    scale_x = screen_width / (x_max - x_min)
    scale_y = screen_height / (y_max - y_min)
    screen_x = (x - x_min) * scale_x
    screen_y = screen_height - (y - y_min) * scale_y
    return int(screen_x), int(screen_y)

x_global_min, x_global_max = -5, 15
y_global_min, y_global_max = -2, 10

running = True
step_index = 0
animation_progress = 0
animation_speed = 10

def draw_axes():
    pygame.draw.line(screen, (200, 200, 200), (0, screen_height // 2), (screen_width, screen_height // 2), 1)  # Ось X
    pygame.draw.line(screen, (200, 200, 200), (screen_width // 2, 0), (screen_width // 2, screen_height), 1)  # Ось Y

    for x in range(x_global_min, x_global_max + 1):
        screen_x, screen_y = to_screen_coords(x, 0, x_global_min, x_global_max, y_global_min, y_global_max)
        label = font.render(str(x), True, (255, 255, 255))
        screen.blit(label, (screen_x - 10, screen_height // 2 + 5))

    for y in range(int(y_global_min), int(y_global_max) + 1):
        screen_x, screen_y = to_screen_coords(0, y, x_global_min, x_global_max, y_global_min, y_global_max)
        label = font.render(str(y), True, (255, 255, 255))
        screen.blit(label, (screen_width // 2 + 5, screen_y - 10))

while running:
    screen.fill((30, 30, 30))

    step = steps[step_index]
    label = font.render(f"Шаг h = {step}", True, (255, 255, 255))
    screen.blit(label, (10, 10))

    draw_axes()

    for name, func in functions.items():
        a, b = intervals[name]
        x_continuous = np.linspace(a, b, 1000)
        y_continuous = func(x_continuous)

        prev_point = None
        for x, y in zip(x_continuous, y_continuous):
            if not (np.isfinite(x) and np.isfinite(y)):
                continue
            screen_x, screen_y = to_screen_coords(x, y, x_global_min, x_global_max, y_global_min, y_global_max)
            if prev_point:
                pygame.draw.line(screen, (100, 100, 255), prev_point, (screen_x, screen_y), 1)
            prev_point = (screen_x, screen_y)

        x_discrete = np.arange(a, b + step, step)
        y_discrete = func(x_discrete)

        for i in range(min(animation_progress, len(x_discrete))):
            x, y = x_discrete[i], y_discrete[i]
            if not (np.isfinite(x) and np.isfinite(y)):
                continue
            screen_x, screen_y = to_screen_coords(x, y, x_global_min, x_global_max, y_global_min, y_global_max)
            pygame.draw.circle(screen, (255, 50, 50), (screen_x, screen_y), 4)

    animation_progress += animation_speed

    if animation_progress > len(x_discrete):
        animation_progress = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                step_index = (step_index + 1) % len(steps)
                animation_progress = 0
            if event.key == pygame.K_LEFT:
                step_index = (step_index - 1) % len(steps)
                animation_progress = 0

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
