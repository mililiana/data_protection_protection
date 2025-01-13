import tkinter as tk
from tkinter import messagebox
from linear_comparison import linear_congruential_generator, find_period, save_to_file
from chesaro import test_chesaro
import random

def get_input_values():
    try:
        a = int(entry_a.get())
        c = int(entry_c.get())
        m = int(entry_m.get())
        X0 = int(entry_X0.get())
        n = int(entry_n.get())
        return a, c, m, X0, n
    except ValueError:
        messagebox.showerror("Помилка", "Перевірте правильність введених даних.")
        return None


def display_and_save_result(text, data):
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, text)
    save_to_file(data)

def generate_numbers():
    input_values = get_input_values()
    if input_values is None:
        return

    a, c, m, X0, n = input_values
    sequence = linear_congruential_generator(a, c, m, X0, n)
    period = find_period(sequence)

    formatted_sequence = "\n".join([", ".join(map(str, sequence[i:i + 10])) for i in range(0, len(sequence), 10)])
    result_text_str = f"Згенерована послідовність:\n{formatted_sequence}\n\nПеріод генератора: {period}"
    display_and_save_result(result_text_str, result_text_str)



def test_chezaro_button():
    input_values = get_input_values()
    if input_values is None:
        return

    a, c, m, X0, n = input_values
    sequence = linear_congruential_generator(a, c, m, X0, n)

    estimated_pi = test_chesaro(sequence, result_text)
    if estimated_pi is None:
        return

    system_sequence = [random.randint(1, m - 1) for _ in range(n)]
    system_estimated_pi = test_chesaro(system_sequence, result_text)
    if system_estimated_pi is None:
        return

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Оцінка значення π для власного генератора: {estimated_pi}\n")
    result_text.insert(tk.END, f"Оцінка значення π для системного генератора: {system_estimated_pi}")

    save_to_file(f"Оцінка значення π для власного генератора: {estimated_pi}\n"
                 f"Оцінка значення π для системного генератора: {system_estimated_pi}")


# Створення вікна
window = tk.Tk()
window.title("Генератор псевдовипадкових чисел")

# Вхідні поля
tk.Label(window, text="Множник (a):").pack()
entry_a = tk.Entry(window)
entry_a.pack()

tk.Label(window, text="Константа (c):").pack()
entry_c = tk.Entry(window)
entry_c.pack()

tk.Label(window, text="Модуль (m):").pack()
entry_m = tk.Entry(window)
entry_m.pack()

tk.Label(window, text="Початкове значення (X0):").pack()
entry_X0 = tk.Entry(window)
entry_X0.pack()

tk.Label(window, text="Кількість чисел (n):").pack()
entry_n = tk.Entry(window)
entry_n.pack()

# Кнопка для запуску генерації
tk.Button(window, text="Генерувати", command=generate_numbers).pack()

# Кнопка для тестування на основі теореми Чезаро
tk.Button(window, text="Тестування Чезаро", command=test_chezaro_button).pack()

# Додавання текстового поля з прокруткою для результатів
result_frame = tk.Frame(window)
result_frame.pack()

# Прокрутка по вертикалі
scrollbar_y = tk.Scrollbar(result_frame)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

# Прокрутка по горизонталі
scrollbar_x = tk.Scrollbar(result_frame, orient=tk.HORIZONTAL)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

# Текстове поле для результатів
result_text = tk.Text(result_frame, wrap=tk.NONE, xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set,
                      height=15, width=70)
result_text.pack()

scrollbar_y.config(command=result_text.yview)
scrollbar_x.config(command=result_text.xview)

# Запуск вікна
window.mainloop()
