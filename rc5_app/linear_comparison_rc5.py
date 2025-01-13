def linear_congruential_generator(a, c, m, seed, n):
    X = seed
    sequence = []
    for _ in range(n):
        X = (a * X + c) % m
        sequence.append(X)
    return sequence