import csv
import datetime
import logging

timestring = datetime.datetime.utcnow().strftime("%Y%m%d_%H_%M_%S")
logfile = 'log_file_' + timestring + '.log'
files_csv = ['gamers_dict_lucky_cube.csv', 'orderdata_sample.csv', 'wrong_file_3.csv', 'orderdata_sample_new.csv', 'wrong_file_1.csv', 'wrong_file_2.csv']

logging.basicConfig(filename=logfile, level=logging.DEBUG)

def read_file(file):
    today = datetime.datetime.today().strftime("%Y-%m-%d %H.%M.%S")
    try:
        with open(file, "r", encoding="utf-8") as fl:
            reader = csv.reader(fl)
            rows = list(reader)
        file_copy = f'{file}_{today}.txt'
        with open(file_copy, 'w', encoding="utf-8", newline='') as fc:
            for row in rows:
                fc.write(' '.join(row) + '\n')
        with open(logfile, 'a', encoding="utf-8", newline='') as log:
            log.write(f'Файл {file} скопирован в {file_copy}. "{today}"' + '\n')
    except FileNotFoundError as err:
        print(f'Файла {file}, не существует')
        logging.error(today + ": " + str(err))

for file in files_csv:
    read_file(file)