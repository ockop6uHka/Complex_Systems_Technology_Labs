import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_bvp

def ode_system(x, y):
    y1, y2 = y
    dy1dx = y2
    dy2dx = x**2 * y2 + (2 / x**2) * y1 + 1 + (4 / x**2)
    return np.vstack((dy1dx, dy2dx))

def boundary_conditions(ya, yb):
    bc1 = 2 * ya[0] - ya[1] - 6  # Граничное условие в точке x=0.5
    bc2 = yb[0] + 3 * yb[1] + 1  # Граничное условие в точке x=1
    return np.array([bc1, bc2])

x = np.linspace(0.5, 1, 100)
y_init = np.zeros((2, x.size))

solution = solve_bvp(ode_system, boundary_conditions, x, y_init)

if solution.status != 0:
    print("Численное решение не удалось получить")
else:
    print("Численное решение получено успешно.")

x_sol = solution.x
y_sol = solution.y[0]
y_prime_sol = solution.y[1]
y_double_prime_sol = ode_system(x_sol, solution.y)[1]

fig, axes = plt.subplots(3, 1, figsize=(10, 8))
fig.suptitle("Анимация решения задачи краевых значений")

titles = ['График функции y(x)', "График первой производной y'(x)", "График второй производной y''(x)"]
colors = ['blue', 'orange', 'green']
y_data = [y_sol, y_prime_sol, y_double_prime_sol]
lines = []

for i, ax in enumerate(axes):
    ax.set_xlim(0.5, 1)
    ax.set_ylim(min(y_data[i]) - 0.5, max(y_data[i]) + 0.5)
    ax.set_title(titles[i])
    ax.set_xlabel('x')
    ax.set_ylabel(titles[i].split()[1])
    ax.grid(True)
    line, = ax.plot([], [], color=colors[i], lw=2, label=titles[i].split()[1])
    lines.append(line)
    ax.legend()

def update(frame):
    for i, line in enumerate(lines):
        line.set_data(x_sol[:frame], y_data[i][:frame])
    return lines

ani = FuncAnimation(fig, update, frames=len(x_sol), interval=50, blit=True)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

x_table = np.linspace(0.5, 1, 10)
y_table = solution.sol(x_table)[0]
y_prime_table = solution.sol(x_table)[1]
y_double_prime_table = ode_system(x_table, solution.sol(x_table))[1]

print(" x       y(x)       y'(x)      y''(x)")
for xi, yi, ypi, ydpi in zip(x_table, y_table, y_prime_table, y_double_prime_table):
    print(f"{xi:.3f}    {yi:.6f}    {ypi:.6f}    {ydpi:.6f}")
