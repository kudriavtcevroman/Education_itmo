# Работа со строками
string1 = 'This is a string.'
string2 = '    This is another string.'
string2 = string2.lstrip()
print(string1, string2, sep='\n')
string3 = string1 + string2
print(string3)

# Извлечение символов и подстрок
name = 'роман'
last_name = 'кудрявцев'
if last_name[-1] == 'a':  # знаю, что это не корректный определитель пола
    print('Привет, уважаемая', name[:-1].title(), last_name[0].upper() + '.')
else:
    print('Привет, уважаемый', name[:-1].title(), last_name[0].upper() + '.')

# Преобразование данных

num_1 = float(input('Введите первое число'))
num_2 = float(input('Введите второе число'))
print('Сумма числа', num_1, 'и числа', num_2, 'равна', num_1 + num_2)

# Форматирование строк

a = 1/3
print("{:7.3f}".format(a))

a = 2/3
b = 2/9
print("{:7.3f} {:7.3f}".format(a, b))
print("{:10.3e} {:10.3e}".format(a, b))

print(f'Сумма числа {num_1} и числа {num_2} равна {num_1 + num_2}')

# Списки

list1 = [82, 8, 23, 97, 92, 44, 17, 39, 11, 12]
list1.append(99)
list1.insert(4, 33)
list1.remove(97)
del list1[-2]
list1 = list1[:5] + list1[7:]
print(list1)
list1.sort()
print(list1)
list2 = list1
list2.sort(reverse=True)
print(list2)

# Кортежи

seq = (2, 8, 23, 97, 92, 44, 17, 39, 11, 12, 8)
print(seq)
print(seq.count(8))
print(seq.index(44))
listseq = list(seq)
print(listseq)
print(type(listseq))
print(type(seq))

# Словари

D = {'food': 'Apple', 'quantity': 4, 'color': 'Red'}
print(D)
print(D['food'])
D['quantity'] += 10
print(D['quantity'])
book = {'Name': [], 'Age': []}
for i in range(3):
    name = input('Введите имя')
    age = int(input('Введите возраст'))
    book['Name'].append(name)
    book['Age'].append(age)
print(book)

# Вложенность хранения данных

rec = {
    'User':{'Name': None, 'Last Name': None},
    'Job':[],
    'Age': None
       }
rec['User']['Name'] = input('Введите имя')
rec['User']['Last Name'] = input('Введите фамилию')
rec['Age'] = int(input('Введите возраст'))
guess = 'да'
while guess.lower() == 'да' or guess.lower() == 'есть':
    job = input('Введите должность')
    rec['Job'].append(job)
    guess = input('У Вас есть еще должности?')
print(rec)