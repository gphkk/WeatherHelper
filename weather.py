import random
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidget, QVBoxLayout
from pyowm import OWM
from pyowm.utils.config import get_default_config

from itertools import groupby

config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = OWM('ae157399507a8eb91962b38584164cf6', config_dict)
mgr = owm.weather_manager()


class Window2(QMainWindow):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.main = root
        self.setWindowTitle("История запросов")
        self.setLayout(QVBoxLayout(self))
        try:
            with open("favorite.txt", "r", encoding="utf-8") as file:  # Считывает с файла и создает список
                city = file.read().splitlines()
        except:
            print("Ошибка")
            city = []
        self.listCity = QListWidget()
        self.layout().addWidget(self.listCity)
        self.resize(400, 200)
        for item in city:
            self.listCity.addItem(item)
        self.listCity.itemDoubleClicked.connect(self.return_city)

    # def clear_history(self):
    #     open('favorite.txt', 'w').close()

    def return_city(self, item):
        city = item.text()
        self.main.search_item(city)


class MainWindow(QMainWindow, ):

    def __init__(self):
        super().__init__()
        uic.loadUi("clothes_prod.ui", self)
        self.pushButton.clicked.connect(lambda: self.search())
        self.action.triggered.connect(lambda: self.menu_action())
        self.action_2.triggered.connect(lambda: self.clear_history())
        self.lineEdit.returnPressed.connect(lambda: self.search())

    def menu_action(self, **kwargs):  # Показ окна истории запросов
        self.w2 = Window2(self)
        self.w2.show()

    def clear_history(self):
        open('favorite.txt', 'w').close()

    def search_item(self, city):  # Запуск программы по нажатию на город из истории запросов
        self.test(city)
        self.lineEdit.setText(city)

    def search(self):  # Добавление нового города в файл
        place = self.lineEdit.text()
        try:
            with open("favorite.txt", "a", encoding="utf-8") as file:
                file.write(f"{place}\n")
        except:
            pass
        self.test(place)

    def test(self, place):
        try:
            observation = mgr.weather_at_place(place)

            w = observation.weather

            temp = w.temperature('celsius')["temp"]
            temp_feel = w.temperature('celsius')["feels_like"]
            wind = w.wind()["speed"]
            humid = w.humidity
            self.label_4.setText(f"{str(temp)} °C")
            self.label_2.setText(f"В городе {place} сейчас {w.detailed_status}")
            self.wind_humid.setText(f"\nВетер {str(wind)} м/с.\nВлажность {str(humid)} %")
            self.feels_label.setText(f"\nОщущается как {str(temp_feel)} °C")

            summer_top = ["майка", "топ", "футболка"]
            summer_bot = ["шорты", "юбка", "легкие брюки"]
            summer_full = ["комбинезон", "платье"]

            warm_top = ["рубашка", "блуза", "свитшот"]
            warm_bot = ["брюки", "джинсы", "легкие брюки"]
            warm_full = ["комбинезон", "платье", "спортивный костюм"]

            norm_top = ["утеплённая рубашка", "блуза", "футболка с джинсовой курткой"]
            norm_bot = ["брюки", "джинсы", "юбка"]
            norm_full = ["спортивный костюм"]

            cool_top = ["рубашка", "водолазка", "свитер"]
            cool_bot = ["брюки", "джинсы"]
            cool_outer = ["кожаная куртка", "плащ", "пальто"]

            # cold_top = cool_top
            # cold_bot = cool_bot
            cold_outer = ["дубленка", "тёплое пальто", "эко-шуба"]

            winter_top = ["свитер", "флисовая кофта", "толстовка", "водолазка"]
            winter_bot = ["спортивки", "джинсы"]
            winter_outer = ["пуховик", "дубленка", "шуба"]

            if float(temp_feel) > 25:
                self.label_3.setText(
                    f"Жарааа... Идеально подойдет сюда {random.choice(summer_top)}, {random.choice(summer_bot)}"
                    f" или {random.choice(summer_full)}.")

            elif 20 <= float(temp_feel) <= 25:
                if float(wind) < 8 and (w.detailed_status == "ясно" or w.detailed_status == "переменная облачность"):
                    self.label_3.setText(f"Очень тепло! Идеально подойдет сюда {random.choice(summer_top)}, "
                                         f"{random.choice(warm_bot)} или {random.choice(summer_full)}.")
                else:
                    self.label_3.setText(f"Тепло! Идеально подойдет сюда {random.choice(warm_top)}, "
                                         f"{random.choice(warm_bot)} или {random.choice(warm_full)}.")

            elif 13 < float(temp_feel) < 20:
                if float(wind) < 8 and w.detailed_status == "ясно":
                    self.label_3.setText(f"Комфортная погода! Идеально подойдет сюда {random.choice(norm_top)}, "
                                         f"{random.choice(norm_bot)} или {random.choice(norm_full)}.")
                else:
                    self.label_3.setText(f"Комфортная погода! Идеально подойдет сюда {random.choice(cool_top)}, "
                                         f"{random.choice(norm_bot)} или {random.choice(norm_full)}.")

            elif 7 < float(temp_feel) <= 13:
                self.label_3.setText(f"Довольно прохладно. Идеально подойдет сюда {random.choice(cool_top)}, "
                                     f"{random.choice(cool_bot)}, а в качестве верхней одежды будет"
                                     f" {random.choice(cool_outer)}.")

            elif 0 <= float(temp_feel) <= 7:
                if float(wind) < 8 and w.detailed_status == "ясно":
                    self.label_3.setText(
                        f"Холодновато. В таком случае, чтобы не замерзнуть, подойдет {random.choice(cool_top)}, "
                        f"a {random.choice(cool_bot)}, а в качестве верхней одежды будет"
                        f" {random.choice(cool_outer)}. И не забудьте надеть шарф!")
                else:
                    self.label_3.setText(
                        f"Холодновато. В таком случае, чтобы не замерзнуть, подойдет {random.choice(cool_top)}, "
                        f" {random.choice(cool_bot)}, а в качестве верхней одежды будет {random.choice(cold_outer)}.")

            elif -10 <= float(temp_feel) < 0:
                if float(wind) < 10 and w.detailed_status != "ясно" and humid < 70:
                    self.label_3.setText(
                        f"Холодно. В таком случае, чтобы не замерзнуть, подойдет {random.choice(cool_top)}, "
                        f"{random.choice(cool_bot)}, а в качестве верхней одежды будет {random.choice(cold_outer)}."
                        f"Пора надевать шапку!")
                else:
                    self.label_3.setText(
                        f"Уже по-зимнему холодно! В таком случае, чтобы не замерзнуть, подойдет "
                        f"{random.choice(cool_top)}, {random.choice(cool_bot)}, а в качестве верхней одежды будет "
                        f"{random.choice(cold_outer)}. Пора надевать шапку и колготки/подштанники!")

            elif float(temp_feel) < -10:
                if float(wind) < 8 and w.detailed_status != "ясно" and humid < 70:
                    self.label_3.setText(f"Морозно. В таком случае, чтобы не замерзнуть, подойдет "
                                         f"{random.choice(winter_top)}, {random.choice(winter_bot)}, "
                                         f"в качестве верхней одежды будет {random.choice(winter_outer)}, "
                                         f"а также не забудьте про тёплые носки и термобелье под одежду!")
                else:
                    self.label_3.setText(f"Пробирающий до костей мороз... В таком случае, чтобы не замерзнуть, подойдет"
                                         f" {random.choice(winter_top)}, {random.choice(winter_bot)}, "
                                         f"в качестве верхней одежды будет {random.choice(winter_outer)}. "
                                         f"Укутывайтесь до ушей, потеплее и побольше!")

            if float(wind) > 15:
                self.label_3.setText(f"На улице сильный ветер, сегодня лучше посидеть дома.")
            else:
                pass

        except:
            QMessageBox.about(self, "Ошибка!", "Введите название корректно!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
