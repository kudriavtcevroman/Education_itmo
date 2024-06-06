name, last_name = input('Введите имя и фамилию').split()
name = name.title()
last_name = last_name.title()
login = last_name[:4] + name[0]
print(last_name, name, ':', login)