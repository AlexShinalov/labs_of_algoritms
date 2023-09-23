import sys
import random
import time
import xlwt
from openpyxl import Workbook
import pandas as pd
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QComboBox

start_time = time.time()

shop_list = [line.strip() for line in open('C:/Users/snw12/Desktop/brands.txt', 'r', encoding="utf8")]
topic_list = [line.strip() for line in open('C:/Users/snw12/Desktop/topics.txt', 'r', encoding="utf8")]
brands_list = [line.strip() for line in open('C:/Users/snw12/Desktop/brand.txt', 'r', encoding="utf8")]

def generate_random_shopping_data():
    random_int = random.randint(0, 29)
    if random_int <= 9:
        random_topic = random.randint(0, 14)
        random_brand = random.randint(0, 149)

    elif 10 <= random_int <= 19:
        random_topic = random.randint(15, 29)
        random_brand = random.randint(150, 299)

    else:
        random_topic = random.randint(30, 49)
        random_brand = random.randint(300, 499)

    return random_int, random_topic, random_brand

class CreditCardGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Генератор фейковых кредитных карт')
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        # Выбор банка
        self.bank_label = QLabel('Выберите банки:')
        self.bank_combo = QComboBox()
        self.bank_combo.addItems(['VTB', 'Sberbank', 'Alfa-Bank', 'Tinkoff', 'Raiffeisen'])
        layout.addWidget(self.bank_label)
        layout.addWidget(self.bank_combo)

        # Выбор платежных систем
        self.type_label = QLabel('Выберите платежные системы:')
        self.type_combo = QComboBox()
        self.type_combo.addItems(['mastercard', 'visa'])
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_combo)

        # Кнопка для генерации номера карты
        self.generate_button = QPushButton('Сгенерировать номер карты')
        self.generate_button.clicked.connect(self.generate_credit_card)
        layout.addWidget(self.generate_button)

        # Отображение сгенерированного номера карты
        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.central_widget.setLayout(layout)

    def generate_credit_card(self):
        bank = self.bank_combo.currentText()
        card_type = self.type_combo.currentText()
        fake_card = self.generate_fake_credit_card_number(bank, card_type)
        self.result_label.setText(f'Сгенерированный номер карты: {fake_card}')

    def generate_fake_credit_card_number(bank, card_type):
        card_number = random.randint(123456789000, 999999999999)
        card_number = str(card_number)
        if bank == 'VTB':
            if card_type == 'mastercard':
                prefix = '4274'
            else:
                prefix = '4272'
        elif bank == 'Sberbank':
            if card_type == 'mastercard':
                prefix = '5469'
            else:
                prefix = '4276'
        elif bank == 'Alfa-Bank':
            if card_type == 'mastercard':
                prefix = '5106'
            else:
                prefix = '4279'
        elif bank == 'Tinkoff':
            if card_type == 'mastercard':
                prefix = '5189'
            else:
                prefix = '5213'
        elif bank == 'Raiffeisen':
            if card_type == 'mastercard':
                prefix = '5404'
            else:
                prefix = '4273'
        else:
            raise ValueError('Недопустимый банк')

        generated_number = card_number
        full_card_number = prefix + generated_number

        return full_card_number



def get_coordinates(query, city):
    url = f'https://nominatim.openstreetmap.org/search'
    params = {'q': f'{query}, {city}', 'format': 'json'}
    response = requests.get(url, params=params)
    data = response.json()
    if data:
        latitude = round(float(data[0]['lat']), 8)
        longitude = round(float(data[0]['lon']), 8)
        return latitude, longitude
    else:
        return None

def random_shopping_time():
    opening_hour = 10
    closing_hour = 21

    random_hour = random.randint(opening_hour, closing_hour)
    random_minute = random.randint(0, 59)

    shopping_time = f"{random_hour:02d}:{random_minute:02d}"

    return shopping_time

def random_nuber_of_goods():
    random_num=random.randint(1,5)
    return random_num


def generate_realistic_price(category):
    price_ranges = {
        "Смартфон": (10000, 70000),
        "Ноутбук": (30000, 120000),
        "Телевизор": (15000, 80000),
        "Планшет": (7000, 35000),
        "Фотокамера": (5000, 30000),
        "Принтер": (3000, 15000),
        "Кондиционер": (10000, 40000),
        "Холодильник": (15000, 60000),
        "Пылесос": (2000, 10000),
        "Стиральная машина": (10000, 50000),
        "Плеер и аудиотехника": (1000, 5000),
        "Микроволновая печь": (3000, 10000),
        "Видеокамера": (8000, 35000),
        "Монитор": (5000, 25000),
        "Гарнитура": (500, 3000),
        "Крем": (200, 1500),
        "Лосьон": (100, 1000),
        "Пудра": (300, 2000),
        "Тональник": (400, 2500),
        "Маскара": (150, 1000),
        "Тушь": (100, 800),
        "Помада": (200, 1500),
        "Блеск": (150, 1000),
        "Парфюм": (1000, 8000),
        "Гель": (100, 800),
        "Консилер": (300, 2000),
        "Румяна": (200, 1500),
        "Линер": (100, 800),
        "Шампунь": (100, 1000),
        "Основа": (300, 2000),
        "Футболка": (500, 3000),
        "Джинсы": (1000, 5000),
        "Платье": (800, 4000),
        "Куртка": (1500, 8000),
        "Блузка": (600, 3000),
        "Шорты": (400, 2000),
        "Юбка": (600, 3000),
        "Пальто": (1500, 8000),
        "Свитер": (800, 4000),
        "Штаны": (800, 4000),
        "Жилет": (500, 2500),
        "Рубашка": (600, 3000),
        "Шарф": (200, 1500),
        "Плавки": (300, 2000),
        "Ветровка": (1000, 5000),
        "Шапка": (200, 1500),
        "Перчатки": (100, 800),
        "Бикини": (300, 2000),
        "Шляпа": (200, 1500),
        'Костюм': (1500, 8000)
    }

    mean, std_dev = price_ranges.get(category, (100, 50))
    price = round(random.gauss(mean, std_dev), 2)
    price = round(price / 100) * 100
    price += random.choice([99, 5, 0])
    if price < 0:
        price = price * (-1)
    return price



#забиваем список с координатами
cordtime_list = []
for i in range(len(shop_list)):
    query= shop_list[i]
    city = 'Санкт-Петербург'
    coordinates = get_coordinates(query, city)
    latitude, longitude = coordinates
    time_buy = random_shopping_time()
    cordtime_list.append(({latitude}, {longitude}, time_buy) )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CreditCardGeneratorApp()
    ex.show()
    sys.exit(app.exec_())
combined_df = pd.DataFrame()

selected_banks = [self.bank_combo.itemText(i) for i in range(self.bank_combo.count()) if self.bank_combo.itemChecked(i)]
selected_payment_systems = [self.type_combo.itemText(i) for i in range(self.type_combo.count()) if self.type_combo.itemChecked(i)]

for i in range(50):
    shopping_data_list = []
    random_int, random_topic, random_brand = generate_random_shopping_data()

    category = str(topic_list[random_topic])
    price_of = generate_realistic_price(category)

    bank = random.choice(selected_banks)
    card_type = random.choice(selected_payment_systems)
    fake_card = ex.generate_fake_credit_card_number(bank, card_type)


    num_of_goods = random_nuber_of_goods()
    shoping_data = generate_random_shopping_data()

    data = {'Название магазина': [shop_list[random_int]],
            'Координаты и время': [cordtime_list[random_int]],
            'Категория': [topic_list[random_topic]],
            'Бренд': [brands_list[random_brand]],
            'Номер карты': [fake_card],
            'Количество товаров': [num_of_goods],
            'Цена': [price_of*num_of_goods]
            }
    df = pd.DataFrame(data)
    combined_df = pd.concat([combined_df, df], ignore_index=True)


    print(shopping_data_list)
print(combined_df)
combined_df.to_excel('output.xlsx', index=False)
end_time = time.time()
execution_time = end_time - start_time
print(f"Program executed in {execution_time} seconds")




