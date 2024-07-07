import csv


def read_file(file_name):      # функция, которая читает файл с данными и выводит список
    with open(file_name, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        return list(reader)

def check_info_about_farmers_markets(market):     # функция, которая проверяет достаточность информации о рынках
    row_counter = 0
    err_lst = []
    for m in market:
        row_counter += 1
        if len(m) != 59:
            err_lst.append(str(row_counter))
    if len(err_lst) == 0:
        return True
    else:
        return f'В {", ".join(err_lst)} строке(-ах) некорректно введена информация о фермерском рынке'

def add_markets_in_class(market_list):    # функция, которая преобразует список рынков в экземпляры класса "Fermers_market"
    if check_info_about_farmers_markets(market_list):
        fermer_market_classes_list = [Fermers_market(market) for market in market_list]
    return fermer_market_classes_list

def del_table_info(file_info): # функция, которая удаляет шапку таблицы с наименованиями столбцов
    return file_info[1:]

def search(market_list):    # метод осуществления поиска рынка по стране, штату или почтовому индексу
    search_results = []
    search_query = input('''
    По какому параметру осуществлять поиск?
    1 - Город
    2 - Штат
    3 - Индекс''')
    while search_query != '1' and search_query != '2' and search_query != '3':
        search_query = input('''
    Введен некорректный ответ. Повторите попытку.
    По какому параметру осуществлять поиск?
    1 - Город
    2 - Штат
    3 - Индекс''')
    if search_query == '1':
        search_state = input('Введите название города')
        for market in market_list:
            if getattr(market, 'City') == search_state:
                search_results.append(market)
    if search_query == '2':
        search_state = input('Введите название штата')
        for market in market_list:
            if getattr(market, 'State') == search_state:
                search_results.append(market)
    if search_query == '3':
        search_state = input('Введите индекс')
        for market in market_list:
            if getattr(market, 'zip') == search_state:
                search_results.append(market)
    for result in search_results:                  # вывод результатов  (при необходимости удалить)
        print(result)
    return search_results                          # возвращение результатов




class Fermers_market:
    def __init__(self, market_info):
        self.FMID = market_info[0]
        self.MarketName = market_info[1]
        self.Website = market_info[2]
        self.Facebook = market_info[3]
        self.Twitter = market_info[4]
        self.Youtube = market_info[5]
        self.OtherMedia = market_info[6]
        self.Street = market_info[7]
        self.City = market_info[8]
        self.Country = market_info[9]
        self.State = market_info[10]
        self.zip = market_info[11]
        self.Season1Date = market_info[12]
        self.Season1Time = market_info[13]
        self.Season2Date = market_info[14]
        self.Season2Time = market_info[15]
        self.Season3Date = market_info[16]
        self.Season3Time = market_info[17]
        self.Season4Date = market_info[18]
        self.Season4Time = market_info[19]
        self.x = market_info[20]
        self.y = market_info[21]
        self.Location = market_info[22]
        self.Credit = market_info[23]
        self.WIC = market_info[24]
        self.WICcash = market_info[25]
        self.SFMNP = market_info[26]
        self.SNAP = market_info[27]
        self.Organic = market_info[28]
        self.Bakedgoods = market_info[29]
        self.Cheese = market_info[30]
        self.Crafts = market_info[31]
        self.Flowers = market_info[32]
        self.Eggs = market_info[33]
        self.Seafood = market_info[34]
        self.Herbs = market_info[35]
        self.Vegetables = market_info[36]
        self.Honey = market_info[37]
        self.Jams = market_info[38]
        self.Maple = market_info[39]
        self.Meat = market_info[40]
        self.Nursery = market_info[41]
        self.Nuts = market_info[42]
        self.Plants = market_info[43]
        self.Poultry = market_info[44]
        self.Prepared = market_info[45]
        self.Soap = market_info[46]
        self.Trees = market_info[47]
        self.Wine = market_info[48]
        self.Coffee = market_info[49]
        self.Beans = market_info[50]
        self.Fruits = market_info[51]
        self.Grains = market_info[52]
        self.Juices = market_info[53]
        self.Mushrooms = market_info[54]
        self.PetFood = market_info[55]
        self.Tofu = market_info[56]
        self.WildHarvested = market_info[57]
        self.UpdateTime = market_info[58]

    def __repr__(self):    # метод, который выводит основную информацию о рынках
        return(f'''
        Market ID: {self.FMID} 
        Market Name: "{self.MarketName}" 
        Adress:
            Index: {self.zip}
            State: {self.State}
            Country: {self.Country}
            City: {self.City}
            Street: {self.Street}
        Contacts:
            Website: {self.Website} 
            Facebook: {self.Facebook} 
            Twitter: {self.Twitter} 
            Other Media: {self.OtherMedia}''')

    def show_products(self):    # метод, который выводит информацию о том, какие продукты продаются на рынках
        return f'''
        Market ID: {self.FMID} 
        Market Name: "{self.MarketName}" 
        Products:
            Organic: {self.Organic}
            Bakedgoods: {self.Bakedgoods}
            Cheese: {self.Cheese}
            Crafts: {self.Crafts}
            Flowers: {self.Flowers}
            Eggs: {self.Eggs}
            Seafood: {self.Seafood}
            Herbs: {self.Herbs}
            Vegetables: {self.Vegetables}
            Honey: {self.Honey}
            Jams: {self.Jams}
            Maple: {self.Maple}
            Meat: {self.Meat}
            Nursery: {self.Nursery}
            Nuts: {self.Nuts}
            Plants: {self.Plants}
            Poultry: {self.Poultry}
            Prepared: {self.Prepared}
            Soap: {self.Soap}
            Trees: {self.Trees}
            Wine: {self.Wine}
            Coffee: {self.Coffee}
            Beans: {self.Beans}
            Fruits: {self.Fruits}
            Grains: {self.Grains}
            Juices: {self.Juices}
            Mushrooms: {self.Mushrooms}
            PetFood: {self.PetFood}
            Tofu: {self.Tofu}
            WildHarvested: {self.WildHarvested}'''

class User:
    def __init__(self, user_info):
        self.name = user_info[0]
        self.surname = user_info[1]
        self.gender = user_info[2]
        self.age = user_info[3]
        self.phone_number = user_info[4]
        self.email = user_info[5]
        self.password = user_info[6]


    def __repr__(self):    # метод, который выводит основную информацию о пользователях
        return(f'''
        User Name: {self.name} 
        User Surname: {self.surname} 
        Gender: {self.gender}
        Age: {self.age}
        Phone Number: {self.phone_number}
        Email: {self.email}''')

    def dict_create(filename='users_dict.csv'):  # создание пользовательской директории
        with open(filename, 'w', encoding="utf-8", newline='') as ud:
            writer = csv.DictWriter(ud, fieldnames=(
            'User_Name', 'User_Surname', 'Gender', 'Age', 'Phone_Number', 'Email', 'Password'))
            writer.writeheader()

    def registration(filename='users_dict.csv'):  # метод, который добавляет нового пользователя в users_dict.csv
        def user_exists(phone_number, email):  # метод, который проверяет, оригинальность телефона и почты
            with open(filename, 'r', encoding="utf-8", newline='') as ud:
                reader = csv.DictReader(ud)
                for row in reader:
                    if row['Phone_Number'] == phone_number or row['Email'] == email:
                        return True
            return False

        user_info = {'User_Name': None, 'User_Surname': None, 'Gender': None, 'Age': None, 'Phone_Number': None,
                     'Email': None, 'Password': None}
        user_info['User_Name'] = (input('Введите имя').title())
        user_info['User_Surname'] = (input('Введите фамилию').title())
        gender_choice = input('''
        Выберите Ваш пол:
        1 - Мужской
        2 - Женский''')
        while gender_choice != '1' and gender_choice != '2':
            gender_choice = input('''
        Введен некорректный ответ. Повторите попытку.    
        Выберите Ваш пол:
        1 - Мужской
        2 - Женский''')
        if gender_choice == '1':
            user_info['Gender'] = 'M'
        else:
            user_info['Gender'] = 'F'
        user_info['Age'] = int(input('Введите возраст'))
        user_info['Phone_Number'] = input('Введите номер телефона')
        user_info['Email'] = input('Введите Email')
        user_info['Password'] = input('Введите пароль')
        if not user_exists(user_info['Phone_Number'], user_info['Email']):
            with open(filename, 'a', encoding="utf-8", newline='') as ud:
                writer = csv.DictWriter(ud, fieldnames=user_info.keys())
                writer.writerow(user_info)
        else:
            print('Пользователь с таким номером телефона или Email уже усществует')


class Review:
    def __init__(self, user_name, user_surname, market_id, rating, comment):
        self.user_name = user_name
        self.user_surname = user_surname
        self.market_id = market_id
        self.rating = rating
        self.comment = comment


    def __repr__(self):
        return (f'''Review:
        User Name: {self.user_name}
        User Surname: {self.user_surname}
        Shop  Id: {self.market_id}
        Rating: {self.rating}
        Comment: {self.comment}''')

    def to_dict(self):
        return {
            'User_Name': self.user_name,
            'User_Surname': self.user_surname,
            'Market_ID': self.market_id,
            'Rating': self.rating,
            'Comment': self.comment
        }

    def dict_create(filename='review_dict.csv'):  # создание директории с рецензиями
        with open(filename, 'w', encoding="utf-8", newline='') as ud:
            writer = csv.DictWriter(ud, fieldnames=('User_Name', 'User_Surname', 'Market_ID', 'Rating', 'Comment'))
            writer.writeheader()

    def add_to_dict(self, filename='review_dict.csv'):  # метод, который записывает рецензию в review_dict.csv
        fieldnames = {'gamer_name': None, 'total_games': 0, 'total_wins': 0, 'gamer_status': None}
        with open(filename, 'a', encoding="utf-8", newline='') as gd:
            writer = csv.DictWriter(gd, fieldnames=('User_Name', 'User_Surname', 'Market_ID', 'Rating', 'Comment'))
            writer.writerow({'User_Name': self.user_name, 'User_Surname': self.user_surname, 'Market_ID': self.market_id, 'Rating': self.rating, 'Comment': self.comment})

FERMERS_MARKETS_LIBRARY_NAME = 'Export.csv'

FERMERS_MARKETS_LIST = read_file(FERMERS_MARKETS_LIBRARY_NAME)
FERMERS_MARKETS_LIST = del_table_info(FERMERS_MARKETS_LIST)
FERMERS_MARKETS_CLASSES_LIST = add_markets_in_class(FERMERS_MARKETS_LIST)

#for market in FERMERS_MARKETS_CLASSES_LIST:      # проверка информации о наличии продуктов на рынках
#    print(market.show_products())

#search(FERMERS_MARKETS_CLASSES_LIST)     # проверка функционирования поиска

#User.dict_create()    # создание пользовательской директории

#User.registration()     # регистрация пользователя
#Review.dict_create()     # создание директории с рецензиями


#rev_1 = Review('Roman', 'Kudriavtcev', '1019956', '5', 'Greatest market!!!')     # создание экземпляра рецензии
#Review.add_to_dict(rev_1)     # запись рецензии в review_dict.csv