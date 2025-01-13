import tkinter as tk
from tkinter import messagebox


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def test_chesaro(sequence, result_text):
    n = len(sequence)

    if n < 2:
        result_text.insert(tk.END, "Помилка: для обчислення необхідно як мінімум 2 елементи у послідовності.\n")
        messagebox.showerror("Помилка", "Недостатньо даних у послідовності для обчислення π.")
        return None

    count = 0


    for i in range(n - 1):
        if gcd(sequence[i], sequence[i + 1]) == 1:
            count += 1

    probability = count / (n - 1)

    if probability == 0:
        result_text.insert(tk.END, "Помилка: ймовірність дорівнює нулю. Обчислення π неможливе.\n")
        messagebox.showerror("Помилка", "Ймовірність дорівнює нулю. Обчислення π неможливе.")
        return None

    estimated_pi = (6 / probability) ** 0.5
    return estimated_pi
