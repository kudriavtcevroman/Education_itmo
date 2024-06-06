ticket = input('Введите номер билета билета из 6 цифр.')
while len(ticket) != 6 or ticket.isdigit() == False:
    ticket = input('Номер билета введен не корректно. Введите повторно.')
num_1 = 0
num_2 = 0
for i in range(len(ticket) // 2):
    num_1 += int(ticket[i])
for i in range(len(ticket) // 2, len(ticket)):
    num_2 += int(ticket[i])
if num_1 == num_2:
    print('Поздравляю, Ваш билет счастливый!')
else:
    print('Ваш билет несчастливый.')