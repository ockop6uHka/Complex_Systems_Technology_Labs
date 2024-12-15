import pygame
import numpy as np

pygame.init()
screen_width, screen_height = 1000, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Графики функций и их производных")
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

functions = [
    lambda x: np.exp(x ** 2 / 2),
    lambda x: np.sin(3 * x / 5) ** 3,
    lambda x: np.cos(x / (x + 1)) ** 2,
    lambda x: np.log(x + np.sqrt(4 + x ** 2)),
    lambda x: (x * np.arctan(2 * x)) / (x ** 2 + 4),
]

derivatives = [
    lambda x: x * np.exp(x ** 2 / 2),
    lambda x: (3 / 5) * np.sin(3 * x / 5) ** 2 * np.cos(3 * x / 5) * 3,
    lambda x: -2 * np.cos(x / (x + 1)) * np.sin(x / (x + 1)) / ((x + 1) ** 2),
    lambda x: 1 / np.sqrt(4 + x ** 2),
    lambda x: (2 * x ** 2 + np.arctan(2 * x) - 8 * x) / (x ** 2 + 4) ** 2,
]

intervals = [(0, 1), (2, 15), (-5, 5)]
steps = [0.01, 0.005]

def to_screen_coords(x, y, x_min, x_max, y_min, y_max):
    scale_x = screen_width / (x_max - x_min)
    scale_y = screen_height / (y_max - y_min)
    screen_x = (x - x_min) * scale_x
    screen_y = screen_height - (y - y_min) * scale_y
    return int(screen_x), int(screen_y)

running = True
func_index = 0
interval_index = 0
step_index = 0
animation_progress = 0
animation_speed = 10

def draw_axes(x_min, x_max, y_min, y_max):
    pygame.draw.line(screen, (200, 200, 200), (0, screen_height // 2), (screen_width, screen_height // 2), 1)
    pygame.draw.line(screen, (200, 200, 200), (screen_width // 2, 0), (screen_width // 2, screen_height), 1)

    for x in range(int(x_min), int(x_max) + 1):
        screen_x, _ = to_screen_coords(x, 0, x_min, x_max, y_min, y_max)
        label = font.render(str(x), True, (255, 255, 255))
        screen.blit(label, (screen_x - 10, screen_height // 2 + 5))

    for y in range(int(y_min), int(y_max) + 1):
        _, screen_y = to_screen_coords(0, y, x_min, x_max, y_min, y_max)
        label = font.render(str(y), True, (255, 255, 255))
        screen.blit(label, (screen_width // 2 + 5, screen_y - 10))

while running:
    screen.fill((30, 30, 30))

    func = functions[func_index]
    dfunc = derivatives[func_index]
    x_min, x_max = intervals[interval_index]
    step = steps[step_index]

    x = np.arange(x_min, x_max + step, step)
    y = func(x)
    dy_numeric = np.diff(y) / step
    x_numeric = x[:-1]
    dy_analytic = dfunc(x)

    y_min = min(np.min(y), np.min(dy_numeric), np.min(dy_analytic))
    y_max = max(np.max(y), np.max(dy_numeric), np.max(dy_analytic))
    draw_axes(x_min, x_max, y_min, y_max)

    for i in range(min(animation_progress, len(x))):
        if i < len(x_numeric):
            x1, y1 = to_screen_coords(x_numeric[i], dy_numeric[i], x_min, x_max, y_min, y_max)
            pygame.draw.circle(screen, (255, 0, 0), (x1, y1), 3)

        x2, y2 = to_screen_coords(x[i], dy_analytic[i], x_min, x_max, y_min, y_max)
        pygame.draw.circle(screen, (0, 255, 0), (x2, y2), 3)

        x3, y3 = to_screen_coords(x[i], y[i], x_min, x_max, y_min, y_max)
        pygame.draw.circle(screen, (0, 0, 255), (x3, y3), 3)

    animation_progress += animation_speed

    if animation_progress > len(x):
        animation_progress = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                func_index = (func_index + 1) % len(functions)
                interval_index = 0
                step_index = 0
                animation_progress = 0
            elif event.key == pygame.K_LEFT:
                func_index = (func_index - 1) % len(functions)
                interval_index = 0
                step_index = 0
                animation_progress = 0

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
