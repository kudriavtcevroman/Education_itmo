from temp_sensor import measure
def answer(s):
    while s.lower() != 'да' and s.lower() != 'нет':
        print('Введен некорректный ответ. Повторите попытку.')
        s = input()
    return s

data_temp_sensor = {
    'Manufacturer': input('Введите название изготовителя'),
    'Model': input('Введите модель'),
    'Minimum_temparature': float(input('Введите минимальное показание измерения датчика')),
    'Maximum_temparature': float(input('Введите максимальное показание измерения датчика')),
    'Signal_type': input('Введите тип сигнала'),
    'Measures': {}
                    }

time_delay = int(input('Введите периодичность измерений (в секундах)'))
number_of_measure = int(input('Введите количество измерений'))


guess = answer(input('Приступить к измерениям? (да/нет)'))
if guess.lower() == 'нет':
    print('Программа завершила работу')
else:
    print('Программа начала работу')
    data_temp_sensor['Measures'] = measure(number_of_measure, data_temp_sensor['Minimum_temparature'], data_temp_sensor['Maximum_temparature'], time_delay)
    print('Программа завершила работу')
    print(f'''
Информация по измерениям:
    Изготовитель датчика: {data_temp_sensor['Manufacturer']}
    Модель датчика: {data_temp_sensor['Model']}
    Минимальное показание измерения датчика: {data_temp_sensor['Minimum_temparature']}
    Максимальное показание измерения датчика: {data_temp_sensor['Maximum_temparature']}
    Тип сигнала: {data_temp_sensor['Signal_type']}
    
Показания:
        ''')
    for i in range(len(data_temp_sensor['Measures']['temp'])):
        print(f"Температура: {data_temp_sensor['Measures']['temp'][i]}. Дата и время: {data_temp_sensor['Measures']['date'][i]}")