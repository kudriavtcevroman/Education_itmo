import def_lib
if not def_lib.gamers_dict_check():
    def_lib.gamers_dict_create()
number_of_gamers = input('Введите количество игроков')
number_of_rounds = int(input('Сколько раундов хотите сыграть?'))
lst_gamers = def_lib.quantity_gamers(number_of_gamers)
for gamer in lst_gamers:
    if not def_lib.gamer_name_exists(gamer):
        def_lib.gamer_name_create(gamer)
ready_for_game = def_lib.answer(input('Готовы начать игру? (да/нет)'))

while ready_for_game == 'да':
    score = def_lib.game_cube(lst_gamers, number_of_rounds)
    for i in range(len(lst_gamers)):
        def_lib.total_games_increase(lst_gamers[i], 1)
        def_lib.status_edit(lst_gamers[i])
    winner = def_lib.select_winner(lst_gamers, score)
    if winner:
        def_lib.total_wins_increase(winner[0], 1)
    ready_for_game = def_lib.answer(input('Хотите сыграть еще раз? (да/нет)'))
show_stats = def_lib.answer(input('Показать общую таблицу результатов? (да/нет)'))
if show_stats == 'да':
    def_lib.show_stats()
else:
    print('***Программа завершила свою работу***')