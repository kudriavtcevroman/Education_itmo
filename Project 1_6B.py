import csv
from pathlib import Path
from datetime import datetime

work = Path.cwd()
print(work)
for file in work.glob('*.csv'):
    rows = []
    with open(file, "r", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        rows = list(reader)
        print(rows)
        print(file.stem)
    time = datetime.now().strftime('%H_%M_%S_%d_%m_%Y')
    file_copy = f'{file.stem}_{time}.txt'
    with open(file_copy, 'w', encoding="utf-8", newline='') as fl:
        for row in rows:
            fl.write(' '.join(row) + '\n')
    with open('log_file.txt', 'a', encoding="utf-8", newline='') as log_file:
        log_file.write(f'Файл {file.stem} скопирован в {file_copy}. "{time}"' + '\n')