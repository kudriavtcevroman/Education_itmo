from random import random

def auto_move(car_positions: list):
    print('')
    for i in range(len(car_positions)):
        # move car
        if random() > 0.3:
            car_positions[i] += 1
        print('-' * car_positions[i])
def auto():
    time = int(input('Введите время'))
    car_positions = [1, 1, 1]
    while time:
        time -= 1
        print('')
        auto_move(car_positions)

auto()