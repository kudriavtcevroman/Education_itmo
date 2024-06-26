'''
Этот модуль содержит функции для игры "Кубик-Рубик".
Полный список функций, которые содержатся в данном модуле:

gamers_dict_check()
gamers_dict_create()
gamer_name_exists(name: str)
gamer_name_create(name: str)
total_games_increase(name: str, game_value: int)
total_wins_increase(name: str, game_value: int)
status_edit(name: str)
show_total_games(name: str)
show_total_wins(name: str)
show_status(name: str)
show_stats()
answer(answr)
quantity_gamers(x: int)
game_cube(gamers: list, rounds: int)
select_winner(gamers: list, score: list)
answer_menu(select)
menu()
'''

import csv
import os
from random import randint
from time import sleep

def gamers_dict_check():
    '''
    Функция, которая проверяет наличие директории gamers_dict_lucky_cube.csv.

    :return:
    '''

    filename = 'gamers_dict_lucky_cube.csv'
    if not os.path.isfile(filename):
        return False
    else:
        return True

def gamers_dict_create():
    '''
    Функция, которая создаёт директорию в виде файла gamers_dict_lucky_cube.csv,
    в которую записывается информация об игроках.

    :return:
    '''

    filename = 'gamers_dict_lucky_cube.csv'
    gamer_stats = {'gamer_name': None, 'total_games': 0, 'total_wins': 0, 'gamer_status': None}
    with open(filename, 'w', encoding="utf-8", newline='') as gd:
        writer = csv.DictWriter(gd, fieldnames=gamer_stats.keys())
        writer.writeheader()

def gamer_name_exists(name: str):
    '''
    Функция, которая проверяет наличие игрока
    в директории файла gamers_dict_lucky_cube.csv.

    :param name:
    :return:
    '''

    filename = 'gamers_dict_lucky_cube.csv'
    with open(filename, 'r', encoding="utf-8", newline='') as gd:
        reader = csv.DictReader(gd)
        for row in reader:
            if row['gamer_name'] == name:
                return True
    return False

def gamer_name_create(name: str):
    '''
    Функция которая создает нового игрока
    в директории файла gamers_dict_lucky_cube.csv.

    :param name:
    :return:
    '''

    filename = 'gamers_dict_lucky_cube.csv'
    gamer_stats = {'gamer_name': None, 'total_games': 0, 'total_wins': 0, 'gamer_status': None}
    with open(filename, 'a', encoding="utf-8", newline='') as gd:
        writer = csv.DictWriter(gd, fieldnames=gamer_stats.keys())
        writer.writerow({'gamer_name': name, 'total_games': 0, 'total_wins': 0, 'gamer_status': 'Новичок'})

def total_games_increase(name: str, game_value: int):
    '''
    Функция, которая увеличивает количество игр,
    сыгранных определенным игроком.

    :param name:
    :param game_value:
    :return:
    '''

    filename = 'gamers_dict_lucky_cube.csv'
    with open(filename, 'r+', encoding="utf-8", newline='') as gd:
        reader = csv.DictReader(gd)
        data = list(reader)
        for row in data:
            if row['gamer_name'] == name:
                score = row['total_games']
                row['total_games'] = int(score) + game_value
                break
        gd.seek(0)
        writer = csv.DictWriter(gd, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(data)
        gd.truncate()

def total_wins_increase(name: str, game_value: int):
    '''
    Функция, которая увеличивает количество побед у определенного игрока.

    :param name:
    :param game_value:
    :return:
    '''

    filename = 'gamers_dict_lucky_cube.csv'
    with open(filename, 'r+', encoding="utf-8", newline='') as gd:
        reader = csv.DictReader(gd)
        data = list(reader)
        for row in data:
            if row['gamer_name'] == name:
                score = row['total_wins']
                row['total_wins'] = int(score) + game_value
                break
        gd.seek(0)
        writer = csv.DictWriter(gd, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(data)
        gd.truncate()

def status_edit(name: str):
    '''
    Функция, которая изменяет статус игрока
    в зависимости от того, сколько игр тот сыграл.

    :param name:
    :return:
    '''

    filename = 'gamers_dict_lucky_cube.csv'
    status = ('Новичок', 'Юниор', 'Любитель', 'Профессионал', 'Эксперт')
    with open(filename, 'r+', encoding="utf-8", newline='') as gd:
        flag = False
        reader = csv.DictReader(gd)
        data = list(reader)
        for row in data:
            if row['gamer_name'] == name:
                score = row['total_games']
                break
        if 5 <= int(score) < 10:
            row['gamer_status'] = status[1]
            flag = True
        elif 10 <= int(score) < 15:
            row['gamer_status'] = status[2]
            flag = True
        elif 15 <= int(score) < 20:
            row['gamer_status'] = status[3]
            flag = True
        elif 20 <= int(score):
            row['gamer_status'] = status[4]
            flag = True
        if flag:
            gd.seek(0)
            writer = csv.DictWriter(gd, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(data)
            gd.truncate()

def show_total_games(name: str):
    '''
    Функция, которая показывает сколько игр сыграл определённый игрок.

    :param name:
    :return:
    '''

    filename = 'gamers_dict_lucky_cube.csv'
    with open(filename, 'r', encoding="utf-8", newline='') as gd:
        reader = csv.DictReader(gd)
        for row in reader:
            if row['gamer_name'] == name:
                return row['total_games']

def show_total_wins(name: str):
    '''
    Функция, которая показывает сколько игр выиграл определённый игрок.

    :param name:
    :return:
    '''

    filename = 'gamers_dict_lucky_cube.csv'
    with open(filename, 'r', encoding="utf-8", newline='') as gd:
        reader = csv.DictReader(gd)
        for row in reader:
            if row['gamer_name'] == name:
                return row['total_wins']

def show_status(name: str):
    '''
    Функция, которая показывает статус определённого игрока.

    :param name:
    :return:
    '''
    filename = 'gamers_dict_lucky_cube.csv'
    with open(filename, 'r', encoding="utf-8", newline='') as gd:
        reader = csv.DictReader(gd)
        for row in reader:
            if row['gamer_name'] == name:
                return row['gamer_status']

def show_stats():
    '''
    Функция, которая показывает общую статистику игроков,
    которая хранится в файле gamers_dict_lucky_cube.csv.

    :return:
    '''

    with open('gamers_dict_lucky_cube.csv', "r", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        rows = list(reader)
    print('Имя игрока', '|', 'Общее количество игр', '|', 'Количество побед', '|', 'Статус игрока')
    for k in range(1, len(rows)):
        print(rows[k][0].ljust(20), rows[k][1].ljust(21), rows[k][2].ljust(13), rows[k][3])

def answer(answr):
    '''
    Функция, которая корректирует правильность ответа, введенного пользователем.

    :param answr:
    :return:
    '''

    while answr.lower() != 'да' and answr.lower() != 'нет':
        print('Некорректный ответ. Повторите ввод.')
        answr = input()
    return answr

def quantity_gamers(x: int):
    '''
    Функция, которая создает список из игроков
    исходя из количества, которое ей подаётся.

    :param x:
    :return:
    '''

    lst_gamers = [input(f'Введите имя {i + 1}-го игрока') for i in range(int(x))]
    return lst_gamers

def game_cube(gamers: list, rounds: int):
    '''
    Функция, которая реализует модель игры "Кубик-Рубик"

    :param gamers:
    :param rounds:
    :return:
    '''

    total_score = [0 for i in range(len(gamers))]
    for _ in range(rounds):
        for i in range(len(gamers)):
            sleep(2)
            print(f'Кубик бросает {gamers[i]}')
            sleep(2)
            score_gamer = randint(1, 6)
            total_score[i] += score_gamer
            print(f'У {gamers[i]} выпало {score_gamer}')
            sleep(1)
            print(f'Общее количество очков у {gamers[i]} - {total_score[i]}')
    sleep(2)
    for i in range(len(gamers)):
        print(f'{gamers[i]} набрал {total_score[i]} очков.')
    sleep(2)
    return total_score

def select_winner(gamers: list, score: list):
    '''
    Функция, которая определяет победителя.

    :param gamers:
    :param score:
    :return:
    '''

    max_score = max(score)
    winners = list()
    gamers_score = list(zip(gamers, score))
    for i in range(len(gamers_score)):
        if gamers_score[i][1] == max_score:
            winners.append(gamers_score[i])
    if len(winners) >= 2:
        print('Ничья!', 'У', end=' ')
        for winner in winners:
            print(f'{winner[0]}', end=' ')
        print(f'одинаковое количество очков - {max_score}')
        return 'draw'
    else:
        print(f'Выиграл {winners[0][0]}, он набрал {max_score} очков!')
        return winners[0][0], winners[0][1]

def answer_menu(select):
    '''
    Функция, которая корректирует правильность ответа, введенного пользователем.

    :param select:
    :return:
    '''

    while select.lower() != 's' and select.lower() != 'e' and select.lower() != 'g':
        print('Некорректный ввод. Повторите попытку.')
        select = input()
    return select

def menu():
    '''
    Функция, которая реализует основное меню игры "Кубик-Рубик"

    :return:
    '''

    print('''
*****************************   
*                           *
*       Главное меню        *
*                           *
*****************************

"G" - начать игру

"S" - показать общую таблицу результатов

"E" - выход
    ''')

    select = answer_menu(input('Введите команду'))
    return select