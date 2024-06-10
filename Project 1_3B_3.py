poem = []
final_word = None
while True:
    word = input('Введите слово')
    if word.isspace():
        break
    poem.append(word.lower())
for i in range(len(poem)):
    print(poem[i][0], end='')