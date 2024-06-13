import csv

filename = "orderdata_sample.csv"
new_filename = "orderdata_sample_new.csv"

rows = []
with open(filename, "r", encoding="utf-8") as fh:       # открываем файл orderdata_sample.csv
    reader = csv.reader(fh)
    rows = list(reader)

rows[0].append('Total')          # формируем столбец 'Total' и значения в него
for i in range(1, len(rows)):
    rows[i].append(int(rows[i][3]) * float(rows[i][4]) + float(rows[i][5]))


with open(new_filename, "w", encoding="utf-8", newline="") as fh:        # записываем отредактированную таблицу в файл orderdata_sample_new.csv
    writer = csv.writer(fh, quoting=csv.QUOTE_ALL)
    for row in rows:
        writer.writerow(row)

new_rows = []
with open(new_filename, "r", encoding="utf-8") as fh:          # открываем файл orderdata_sample_new.csv
    reader = csv.reader(fh)
    new_rows = list(reader)

for row in new_rows:
    print(row)