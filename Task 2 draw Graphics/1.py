import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp
from sympy import symbols, Function, dsolve, Eq, exp, sin, lambdify, simplify

# Параметры задачи
m = 1.0
k = 1.0
v0 = 1.0
x0 = 0.0
t_span = (0, 20)
t_eval = np.linspace(t_span[0], t_span[1], 400)

# Коэффициенты демпфирования
h_under = 1.0  # h^2 < 4km
h_over = 4.0   # h^2 > 4km

forces = [
    {'name': 'f(t) = 0', 'f_expr': 0, 'f_func': lambda t: 0},
    {'name': 'f(t) = t - 1', 'f_expr': symbols('t') - 1, 'f_func': lambda t: t - 1},
    {'name': 'f(t) = e^{-t}', 'f_expr': exp(-symbols('t')), 'f_func': lambda t: np.exp(-t)},
    {'name': 'f(t) = sin(t)', 'f_expr': sin(symbols('t')), 'f_func': lambda t: np.sin(t)}
]

def analytical_solution(h, f_expr):
    t = symbols('t', real=True)
    x = Function('x')(t)
    f = f_expr
    eq = Eq(m * x.diff(t, t) + h * x.diff(t) + k * x, f)
    ics = {x.subs(t, 0): x0, x.diff(t).subs(t, 0): v0}
    sol = dsolve(eq, x, ics=ics)
    x_t = simplify(sol.rhs)
    x_func = lambdify(t, x_t, modules=['numpy'])
    return x_func

def numerical_solution(h, f_func):
    def ode_system(t, y):
        x1, x2 = y
        dx1dt = x2
        dx2dt = (f_func(t) - h * x2 - k * x1) / m
        return [dx1dt, dx2dt]

    y0 = [x0, v0]
    sol = solve_ivp(ode_system, t_span, y0, t_eval=t_eval)
    return sol.t, sol.y[0]

def animate_solution(force, h_under, h_over):
    force_name = force['name']
    f_expr = force['f_expr']
    f_func = force['f_func']

    x_analytical_under = analytical_solution(h_under, f_expr)
    _, x_num_under = numerical_solution(h_under, f_func)

    x_analytical_over = analytical_solution(h_over, f_expr)
    _, x_num_over = numerical_solution(h_over, f_func)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    plt.suptitle(f"Force: {force_name}", fontsize=14)

    ax1, ax2 = axes
    ax1.set_title(f"Underdamped (h^2 < 4km)")
    ax2.set_title(f"Overdamped (h^2 > 4km)")

    for ax in axes:
        ax.set_xlim(t_span)
        ax.set_ylim(-3, 3)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Displacement (m)")

    line_ana_under, = ax1.plot([], [], 'g-', label='Аналитическое')
    line_num_under, = ax1.plot([], [], 'r--', label='Численное')
    line_ana_over, = ax2.plot([], [], 'g-', label='Аналитическое')
    line_num_over, = ax2.plot([], [], 'r--', label='Численное')

    ax1.legend()
    ax2.legend()

    def update(frame):
        t_slice = t_eval[:frame]
        line_ana_under.set_data(t_slice, x_analytical_under(t_slice))
        line_num_under.set_data(t_slice, x_num_under[:frame])
        line_ana_over.set_data(t_slice, x_analytical_over(t_slice))
        line_num_over.set_data(t_slice, x_num_over[:frame])
        return line_ana_under, line_num_under, line_ana_over, line_num_over

    anim = FuncAnimation(fig, update, frames=len(t_eval), interval=20, blit=True)
    plt.show()

for force in forces:
    animate_solution(force, h_under, h_over)
