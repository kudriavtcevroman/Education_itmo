def nod(a, b):
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a

num_1, num_2 = int(input('Задайте первое число ')), int(input('Задайте второе число '))

print('НОД равен', nod(num_1, num_2))