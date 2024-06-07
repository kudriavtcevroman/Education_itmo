from time import asctime, sleep
from refrigerator import temperature
def measure(number_of_measure, temp_min, temp_max, time_delay):
    data = {'date': [], 'temp': []}
    for i in range(number_of_measure):
        t = temperature(temp_min, temp_max)
        time = asctime()
        data['date'].append(time)
        data['temp'].append(t)
        print(f"Температура: {data['temp'][i]}. Дата и время: {data['date'][i]}")
        sleep(time_delay)
    return data
