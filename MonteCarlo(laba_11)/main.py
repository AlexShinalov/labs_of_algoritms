import random
import tkinter as tk
import math
import scipy.integrate as spi
import numpy as np

def is_inside(x, y):
    return (-x**3 - y**4 < 2) and (3*x + y**2 < 2) and (-2 < x < 2) and (-2 < y < 2)

def generate_point():
    return random.uniform(-2, 2), random.uniform(-2, 2)

def monte_carlo_area(N):
    k = 0
    for _ in range(N):
        x, y = generate_point()
        if is_inside(x, y):
            k += 1
    S0 = 16
    S = k / N * S0
    return S

def integrand(x):
    return math.cos(2 * x)

def monte_carlo_integral(N):
    integral = 0
    for _ in range(N):
        x = random.uniform(0, math.cos(math.pi / 4))
        integral += integrand(x)
    integral *= math.cos(math.pi / 4) / N
    return integral

def run_monte_carlo_area():
    N = int(entry_area.get())
    area = monte_carlo_area(N)
    result_area.config(text=f"Площадь: {area}")

def run_monte_carlo_integral():
    N = int(entry_integral.get())
    integral = monte_carlo_integral(N)
    result_integral.config(text=f"Интеграл: {integral}")

def integradd(x):
    return np.cos(2*x)

def regular_integral():
    result, _ = spi.quad(integradd, 0, np.cos(np.pi/4))
    result_integral_2.config(text=f"Интеграл: {result}")

root = tk.Tk()
root.title("MonteCarlo")


frame_area = tk.Frame(root)
frame_area.pack(pady=10)

label_area = tk.Label(frame_area, text="Введите число N:")
label_area.grid(row=0, column=0)

entry_area = tk.Entry(frame_area)
entry_area.grid(row=0, column=1)

button_area = tk.Button(frame_area, text="Вычислить площадь", command=run_monte_carlo_area)
button_area.grid(row=0, column=2)

result_area = tk.Label(frame_area, text="")
result_area.grid(row=1, columnspan=3)

frame_integral = tk.Frame(root)
frame_integral.pack(pady=10)

label_integral = tk.Label(frame_integral, text="Введите число N:")
label_integral.grid(row=0, column=0)

entry_integral = tk.Entry(frame_integral)
entry_integral.grid(row=0, column=1)

button_integral = tk.Button(frame_integral, text="Вычислить интеграл", command=run_monte_carlo_integral)
button_integral.grid(row=0, column=2)

result_integral = tk.Label(frame_integral, text="")
result_integral.grid(row=1, columnspan=3)

button_integral = tk.Button(frame_integral, text="Проверка", command=regular_integral)
button_integral.grid(row=0, column=4)

result_integral_2 = tk.Label(frame_integral, text="")
result_integral_2.grid(row=2, columnspan=4)

root.mainloop()

