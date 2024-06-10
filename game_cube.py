from random import randint
from time import sleep
def answer(s):
    while s.lower() != 'да' and s.lower() != 'нет':
        print('Некорректный ответ. Повторите ввод.')
        s = input()
    return s
gamer_stats = {'Gamer_1_name': None, 'Gamer_1_score': 0, 'Gamer_2_name': None, 'Gamer_2_score': 0}
gamer_1 = input('Введите имя первого игрока').title()
gamer_2 = input('Введите имя второго игрока').title()
gamer_stats['Gamer_1_name'] = gamer_1
gamer_stats['Gamer_2_name'] = gamer_2
sleep(1)
sleep(1)
print('Начнём игру?')
guess = answer(input())
while guess == 'да':
    number_of_batches = int(input('Сколько партий Вы хотите сыграть?'))
    total_score_gamer_1 = 0
    total_score_gamer_2 = 0
    for _ in range(number_of_batches):
        sleep(2)
        print(f'Кубик бросает {gamer_1}')
        sleep(2)
        score_gamer_1 = randint(1, 6)
        total_score_gamer_1 += score_gamer_1
        print(f'У {gamer_1} выпало {score_gamer_1}')
        sleep(3)
        print(f'Кубик бросает {gamer_2}')
        sleep(2)
        score_gamer_2 = randint(1, 6)
        total_score_gamer_2 += score_gamer_2
        print(f'У {gamer_2} выпало {score_gamer_2}')
        sleep(1)
        print(f'У {gamer_1} {total_score_gamer_1} очков, у {gamer_2} {total_score_gamer_2} очков')
        sleep(1)
    gamer_stats['Gamer_1_score'] += total_score_gamer_1
    gamer_stats['Gamer_2_score'] += total_score_gamer_2
    if total_score_gamer_1 > total_score_gamer_2:
        print(f'Победил {gamer_1}!')
    elif total_score_gamer_1 < total_score_gamer_2:
        print(f'Победил {gamer_2}!')
    else:
        print('Ничья!')
    sleep(2)
    print('Хотите сыграть еще раз?')
    guess = answer(input())
print('Игра окончена')
print(gamer_stats)