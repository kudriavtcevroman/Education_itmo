import re

def clean(word):
    return re.sub(r"[`!?.:;,'\"()-]", "", word.strip())
total_rows = 0
total_alpha = 0
filename = 'file.txt'
F = open(filename, 'r')
lst = []
for row in F:
    if '\n' in row:
        total_rows+= 1
    lst.append(row.rstrip().lower())

word = map(clean, lst)
text = ' '.join(word)
total_words = len(text.split())
for w in text:
    total_alpha += len(w)
print(f'Число строк: {total_rows}')
print(f'Число слов: {total_words}')
print(f'Число букв: {total_alpha}')