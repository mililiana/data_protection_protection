import os

def linear_congruential_generator(a, c, m, seed, n):
    X = seed
    sequence = []
    for _ in range(n):
        X = (a * X + c) % m
        sequence.append(X)
    return sequence

def find_period(sequence):
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[0]:
            return i
    return len(sequence)

def save_to_file(content, filename="result.txt"):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(project_dir, filename)

    with open(file_path, 'w') as file:
        file.write(content)

    print(f"Результат збережений у файл: {file_path}")
