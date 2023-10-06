import pandas as pd
import random
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox


"""class AnonymizationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.actionLabel = QLabel('Выберите действие:')
        self.actionComboBox = QComboBox()
        self.actionComboBox.addItem('Обезличить датасет')
        self.actionComboBox.addItem('Вычислить k-анонимность')

        self.qiLabel = QLabel('Введите Квази-идентификаторы (через запятую):')
        self.qiInput = QLineEdit()

        self.executeButton = QPushButton('Выполнить')
        self.executeButton.clicked.connect(self.executeAction)

        layout.addWidget(self.actionLabel)
        layout.addWidget(self.actionComboBox)
        layout.addWidget(self.qiLabel)
        layout.addWidget(self.qiInput)
        layout.addWidget(self.executeButton)

        self.setLayout(layout)
        self.setWindowTitle('Anonymization App')
        self.show()

    def executeAction(self):
        action = self.actionComboBox.currentText()
        qi_identifiers = self.qiInput.text().split(',')

        if action == 'Обезличить датасет':
            # Выполнить обезличивание
            pass
        elif action == 'Вычислить k-анонимность':
            # Выполнить вычисление k-анонимности с использованием qi_identifiers
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AnonymizationApp()
    sys.exit(app.exec_())"""

# Чтение данных из файлов
st = [line.strip() for line in open('C:/Users/snw12/Desktop/brands.txt', 'r', encoding="utf8")]
shop_list = [line.strip() for line in open('C:/Users/snw12/Desktop/brands.txt', 'r', encoding="utf8")]
topic_list = [line.strip() for line in open('C:/Users/snw12/Desktop/topics.txt', 'r', encoding="utf8")]

excel_data_df = pd.read_excel('output.xlsx', sheet_name='Sheet1')
columns = ['Название магазина', 'Координаты и время', 'Категория', 'Бренд', 'Номер карты', 'Количество товаров', 'Цена']

def mask_mag(data):
    for i in range(len(shop_list)):
        if shop_list[i]==data:
            index=i
            if index <=9:
                masked_data='Техники'
            elif 10<=index<=19:
                masked_data = 'Косметики и мед.товаров'
            elif index>19:
                masked_data ="Одежды"

    return masked_data

def mask_shop(data):
    for i in range(len(topic_list)):
        if topic_list[i]==data:
            index=i
            if index <=14:
                masked_data='Техника'
            elif 14<index<=29:
                masked_data = 'Косметика и медицина'
            elif index>29:
                masked_data ="Одежда,обувь и аксессуары"

    return masked_data

def generate_realistic_price(data):
    price_ranges = {
        "Смартфон": (10000, 120000),
        "Ноутбук": (10000, 120000),
        "Телевизор": (10000, 120000),
        "Планшет": (500, 35000),
        "Фотокамера": (500, 35000),
        "Принтер": (500, 35000),
        "Кондиционер": (10000, 120000),
        "Холодильник": (10000, 120000),
        "Пылесос": (500, 35000),
        "Стиральная машина": (10000, 120000),
        "Плеер и аудиотехника": (500, 35000),
        "Микроволновая печь": (500, 35000),
        "Видеокамера": (500, 35000),
        "Монитор": (500, 35000),
        "Гарнитура": (500, 35000),
        "Крем": (100, 2500),
        "Лосьон": (100, 2500),
        "Пудра": (100, 2500),
        "Тональник": (100, 2500),
        "Маскара": (100, 2500),
        "Тушь": (100, 1000),
        "Помада": (100, 1000),
        "Блеск": (100, 1000),
        "Парфюм": (1000, 8000),
        "Гель": (100, 1000),
        "Консилер": (100, 2500),
        "Румяна": (100, 2500),
        "Линер": (100, 1000),
        "Шампунь": (100, 1000),
        "Основа": (100, 2500),
        "Футболка": (500, 5000),
        "Джинсы": (1000, 8000),
        "Платье": (1000, 8000),
        "Куртка": (500, 5000),
        "Блузка": (500, 5000),
        "Шорты": (500, 5000),
        "Юбка": (500, 5000),
        "Пальто": (1000, 8000),
        "Свитер": (1000, 8000),
        "Штаны": (500, 5000),
        "Жилет": (500, 2500),
        "Рубашка": (500, 5000),
        "Шарф": (100, 2500),
        "Плавки": (100, 2500),
        "Ветровка": (500, 5000),
        "Шапка": (100, 2500),
        "Перчатки": (100, 2500),
        "Бикини": (100, 2500),
        "Шляпа": (100, 2500),
        'Костюм': (1000, 8000)
    }

    price = price_ranges.get(data)

    return price

def mask_data(data):
    masked_data_1 = "*" * 12
    pref = str(data)[:4]
    masked_data = pref + masked_data_1
    return masked_data

def how_much(data):
    if int(data) >= 3:
        masked_data = '>=3'
    else:
        masked_data = '<3'
    return masked_data

def del_brand(data):
    if data != ' ':
        masked_data = ' '
    return masked_data

def perturb_data(data):
    data = str(data)
    start_index = data.find('.') + 1
    startstart_index = data.find('.', start_index) + 1
    end_index = data.find(',', start_index)
    ednend_index = data.find("'")
    time_end = data.find("'", ednend_index)

    first_cord = data[start_index:end_index]
    second_cord = data[startstart_index:ednend_index]

    perturbed_data1 = ''.join(char if random.random() > 0.2 else random.choice("1234567890") for char in first_cord)
    perturbed_data2 = ''.join(char if random.random() > 0.2 else random.choice("1234567890") for char in second_cord)

    first_cord = data[1:4] + perturbed_data1
    second_cord = data[end_index:startstart_index] + perturbed_data2
    cord = first_cord[:2] + second_cord[:4]

    return cord

def calculate_k_anonymity(df, k):
    group_counts = df.groupby(columns).size().reset_index(name='count')
    return all(group_counts['count'] >= k)

# Преобразование данных
for i in range(1):
    excel_data_df['Название магазина'] = excel_data_df['Название магазина'].apply(mask_mag)
    excel_data_df['Цена'] = excel_data_df['Категория'].apply(generate_realistic_price)
    excel_data_df['Категория'] = excel_data_df['Категория'].apply(mask_shop)
    excel_data_df['Номер карты'] = excel_data_df['Номер карты'].apply(mask_data)
    excel_data_df['Координаты и время'] = excel_data_df['Координаты и время'].apply(perturb_data)
    excel_data_df['Количество товаров'] = excel_data_df['Количество товаров'].apply(how_much)
    excel_data_df['Бренд'] = excel_data_df['Бренд'].apply(del_brand)


excel_data1_df = excel_data_df.copy()  # Make a copy for further calculations
k = 7
k_anon = calculate_k_anonymity(excel_data1_df, k)
print(f"Датасет {'соответствует' if k_anon else 'не соответствует'} {k}-анонимности.")


group_counts = excel_data1_df.groupby(columns).size().reset_index(name='count')
bad_k_values = group_counts[group_counts['count'] < k].head(5)

percentage_bad_k = (len(bad_k_values) / len(group_counts)) * 100

print(f"\nПлохие значения K-анонимности (первые 5):")
print(bad_k_values)
print(f"\nПроцент 'плохих' значений K-анонимности: {percentage_bad_k:.2f}%")

unique_rows_count = len(excel_data1_df.groupby(columns))

print(f"\nКоличество уникальных строк по квази-идентификаторам: {unique_rows_count}")

if k == 1:
    unique_rows = excel_data1_df.groupby(columns).size().reset_index()
    print("\nУникальные строки:")
    print(unique_rows)

excel_data_df.to_excel('output2.xlsx', index=False)
