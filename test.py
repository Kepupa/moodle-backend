алек только надо вроде как pyqt6 я хз какая у вас но если чо будь внимателен, там всё одинаковое просто 5 поменять на 6
и если чо пиши в ридмишке, я обновляю 3 мин каждые



import sys
import psycopg2
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QSizePolicy, QScrollArea
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt

DB_CONFIG = {
    'dbname': 'your_db_name',
    'user': 'your_db_user',
    'password': 'your_db_password',
    'host': 'localhost',
    'port': 5432
}

def get_products_with_cost():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    # Получение продукции с типом
    cur.execute("""
        SELECT p.id, pt.product_type, p.product_name, p.articul, p.minimal_cost_for_partner, p.roll_width
        FROM products p
        JOIN product_types pt ON p.product_type_id = pt.id
        ORDER BY p.id
    """)
    products = cur.fetchall()
    result = []
    for prod in products:
        prod_id, prod_type, prod_name, articul, min_cost, roll_width = prod
        # Расчет стоимости исходя из материалов
        cur.execute("""
            SELECT pm.required_amount_of_material, m.price_per_unit_of_material
            FROM product_materials pm
            JOIN materials m ON pm.material_id = m.id
            WHERE pm.product_id = %s
        """, (prod_id,))
        materials = cur.fetchall()
        cost = sum(req * price for req, price in materials)
        cost = round(cost, 2)
        if cost < 0:
            cost = 0.0
        result.append({
            'type': prod_type,
            'name': prod_name,
            'articul': articul,
            'min_cost': min_cost,
            'roll_width': roll_width,
            'cost': cost
        })
    cur.close()
    conn.close()
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
        self.setWindowIcon(QIcon("icon.png"))  # Путь к иконке приложения
        self.resize(700, 500)
        main_layout = QVBoxLayout()
        # Логотип компании (если есть)
        logo = QPixmap("logo.png")  # Путь к логотипу
        if not logo.isNull():
            logo_label = QLabel()
            logo_label.setPixmap(logo.scaledToHeight(60, Qt.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(logo_label)
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
