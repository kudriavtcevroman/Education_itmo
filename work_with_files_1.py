import os

folder = r'D:\Обучение Python\test'
answ = set()
search = input('Введите поисковой запрос')


for filename in os.listdir(folder):
    filepath = os.path.join(folder, filename)
    with open(filepath, 'r', encoding="utf-8") as fp:
        for line in fp:
            if search in line:
                answ.add(filename)

for i in answ:
 print(i)
