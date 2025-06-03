import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QScrollArea
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt

# Фиктивные данные вместо БД
def get_products_with_cost():
    # Список продуктов с материалами и ценами (пример)
    products = [
        {
            'id': 1,
            'type': 'Тип продукта A',
            'name': 'Продукт 1',
            'articul': 12345,
            'min_cost': 100.00,
            'roll_width': 1.5,
            'materials': [
                {'required_amount': 2.0, 'price_per_unit': 50.0},
                {'required_amount': 1.0, 'price_per_unit': 20.0}
            ]
        },
        {
            'id': 2,
            'type': 'Тип продукта B',
            'name': 'Продукт 2',
            'articul': 67890,
            'min_cost': 200.00,
            'roll_width': 2.0,
            'materials': [
                {'required_amount': 3.0, 'price_per_unit': 30.0},
                {'required_amount': 2.0, 'price_per_unit': 40.0}
            ]
        }
    ]

    result = []
    for prod in products:
        cost = sum(m['required_amount'] * m['price_per_unit'] for m in prod['materials'])
        cost = round(cost, 2)
        if cost < 0:
            cost = 0.0
        result.append({
            'type': prod['type'],
            'name': prod['name'],
            'articul': prod['articul'],
            'min_cost': prod['min_cost'],
            'roll_width': prod['roll_width'],
            'cost': cost
        })
    return result

class ProductCard(QFrame):
    def __init__(self, product):
        super().__init__()
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(1)
        self.setStyleSheet("background-color: white;")
        layout = QHBoxLayout()
        left = QVBoxLayout()
        # Заголовок
        header = QLabel(f"{product['type']} | {product['name']}")
        header.setFont(QFont('Arial', 11, QFont.Bold))
        left.addWidget(header)
        # Подписи
        articul = QLabel(f"Артикул: {product['articul']}")
        min_cost = QLabel(f"Минимальная стоимость для партнера (₽): {product['min_cost']}")
        roll_width = QLabel(f"Ширина (м): {product['roll_width']}")
        for lbl in (articul, min_cost, roll_width):
            lbl.setFont(QFont('Arial', 9))
            left.addWidget(lbl)
        left.addStretch()
        layout.addLayout(left)
        # Стоимость справа
        right = QVBoxLayout()
        cost_label = QLabel(f"Стоимость (₽)\n{product['cost']:.2f}")
        cost_label.setFont(QFont('Arial', 11, QFont.Bold))
        cost_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        right.addWidget(cost_label)
        right.addStretch()
        layout.addLayout(right)
        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Продукция компании")
        # self.setWindowIcon(QIcon("icon.png"))  # Иконка, если есть
        self.resize(700, 500)
        main_layout = QVBoxLayout()
        # Логотип компании (если есть)
        # logo = QPixmap("logo.png")
        # if not logo.isNull():
        #     logo_label = QLabel()
        #     logo_label.setPixmap(logo.scaledToHeight(60, Qt.SmoothTransformation))
        #     logo_label.setAlignment(Qt.AlignCenter)
        #     main_layout.addWidget(logo_label)
        # Заголовок
        title = QLabel("Список продукции")
        title.setFont(QFont('Arial', 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        # Прокручиваемая область для карточек продукции
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        vbox = QVBoxLayout()
        products = get_products_with_cost()
        for prod in products:
            card = ProductCard(prod)
            vbox.addWidget(card)
        vbox.addStretch()
        content.setLayout(vbox)
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
