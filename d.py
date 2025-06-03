import psycopg2

from partners_type import Product, Partner, Sale

# Press the green button in the gutter to run the script.
def connect_db():
    return psycopg2.connect(
        dbname="demo",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )

def fetch_data():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        # Мне кажется, что так будет проще создать объект, а то вот так вот через x[..], выглядит страшно...
        cursor.execute("SELECT product_type_id, product_name, minimum_cost_for_partner FROM products")
        product_data = [Product(*row) for row in cursor.fetchall()]


        cursor.execute("SELECT partner_type, partner_name, director, partner_email, partner_phone, partner_adress, inn, rating FROM partners")
        partners_data = [Partner(*row) for row in cursor.fetchall()]


        cursor.execute("SELECT partner_id, product_id, quantity_of_production FROM partner_products")
        sale_data = [Sale(*row) for row in cursor.fetchall()]

        cursor.close()
        connection.close()
        return product_data, partners_data, sale_data

    except psycopg2.Error as e:
        print("Ошибка подключения к базе данных!", e)



if __name__ == "__main__":
    products, partners, sales = fetch_data()


    for sale in sales:
        discount = sale.calculate_discount()
        print(f"Партнер {sale.partner_id} купил продукт {sale.product_id} → скидка {discount}%")
class Partner:

    def __init__(self, partner_type, name, director, email, phone, adress, inn, rating):
        self.partner_type = partner_type
        self.name = name
        self.director = director
        self.email = email
        self.phone = phone
        self.adress = adress
        self.inn = inn
        self.rating = rating


class Product:

    def __init__(self, name, articul, min_cost):
        self.name = name
        self.articul = articul
        self.min_cost = min_cost


class Sale:
    def __init__(self, partner_id, product_id, quantity):
        self.partner_id = partner_id
        self.product_id = product_id
        self.quantity = quantity

    def calculate_discount(self):
        if self.quantity >= 1000:
            return 15
        elif self.quantity >= 500:
            return 10
        elif self.quantity >= 100:
            return 5
        return 0

//main_window

from PyQt6.QtGui import QIcon
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QListWidgetItem, QMainWindow, QWidget

import engine
from edit_window import Ui_EditWindow
from list_view import PartnerItemWidget
from db import get_partners


class Ui_MainWindow(object):
    def setupUi(self, MainWindow : QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Подмодуль партнёры")
        MainWindow.resize(800, 600)
        MainWindow.setWindowIcon(QIcon('res/icon.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.edit_window = QWidget()
        self.edit_window_ui = Ui_EditWindow()
        self.edit_window_ui.setupUi(self.edit_window)
        self.edit_window_ui.back_button.clicked.connect(get_new_partner_data)
        self.centralwidget.setObjectName("centralwidget")
        self.listView = QtWidgets.QListWidget(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(10, 10, 781, 551))
        self.listView.setObjectName("listView")
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(360, 520, 141, 24))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.create_new_partner)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def create_new_partner(self):
        self.edit_window_ui.fill_partner()
        self.edit_window.show()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def add_item(self, partner):
        item = QListWidgetItem()
        item.setSizeHint(QSize(300, 150))
        self.listView.addItem(item)

        widget = PartnerItemWidget()
        widget.setupUi(self.edit_window, self.edit_window_ui, partner)

        self.listView.setItemWidget(item, widget)

    def clear_list(self):
        self.listView.clear()


ui = Ui_MainWindow()

def setupUI(partners):
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui.setupUi(MainWindow)

    for partner in partners:
        ui.add_item(partner)

    MainWindow.show()
    app.exec()
    sys.exit(app.exec())

def get_new_partner_data():
    ui.clear_list()
    partner_data = get_partners()

    for partner in partner_data:
        engine.calculate_discount(partner)
        ui.add_item(partner)
