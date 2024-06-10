import random
lst = list()
volume = ['High', 'Low']
for _ in range(10):
    lst.append(random.randint(1, 100))
print(lst)
threshold_value = int(input('Введите пароговое значение (от 1 до 100)'))
for i in range(len(lst)):
    if lst[i] > threshold_value:
        print(f'Число {lst[i]} имеет значение {volume[0]}')
    elif lst[i] < threshold_value:
        print(f'Число {lst[i]} имеет значение {volume[1]}')
    else:
        print(f'Число {lst[i]} равно пороговому значению')
