import sys
import psycopg2
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QFrame
)
from PyQt6.QtGui import QIcon, QPixmap

DB_CONFIG = {
    "user": "postgres",
    "password": "your_password",
    "host": "localhost",
    "port": "5432",
    "database": "your_database"
}

def fetch_products():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    # Получаем все продукты с нужными полями и id
    cursor.execute("""
        SELECT 
            p.product_id, pt.product_type, p.product_name, p.articul, 
            p.min_cost_for_partner, mt.material_type
        FROM products p
        JOIN product_types pt ON p.product_type_id = pt.product_type_id
        JOIN material_types mt ON p.material_type_id = mt.material_type_id
    """)
    products = cursor.fetchall()
    # Для каждого продукта получаем сумму времени изготовления
    product_list = []
    for prod in products:
        product_id = prod[0]
        cursor.execute("""
            SELECT COALESCE(SUM(time_todo), 0)
            FROM product_workshops
            WHERE product_id = %s
        """, (product_id,))
        total_time = cursor.fetchone()[0]
        product_list.append((*prod[1:], total_time))
    cursor.close()
    conn.close()
    return product_list

class ProductCard(QFrame):
    def __init__(self, product):
        super().__init__()
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(1)
        left = QVBoxLayout()
        title = QLabel(f"{product[0]} | {product[1]}")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        left.addWidget(title)
        left.addWidget(QLabel(f"Артикул: {product[2]}"))
        left.addWidget(QLabel(f"Минимальная стоимость для партнера: {product[3]}"))
        left.addWidget(QLabel(f"Основной материал: {product[4]}"))
        main = QHBoxLayout()
        main.addLayout(left)
        main.addStretch()
        right = QVBoxLayout()
        right.addWidget(QLabel(f"Время изготовления"))
        right.addWidget(QLabel(f"{product[5]} ч."))
        main.addLayout(right)
        self.setLayout(main)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Продукция компании")
        self.setWindowIcon(QIcon("app_icon.png"))  # путь к иконке приложения
        layout = QVBoxLayout()
        # Логотип компании
        logo = QLabel()
        logo.setPixmap(QPixmap("company_logo.png").scaledToHeight(50))
        layout.addWidget(logo)
        # Прокручиваемая область для карточек
        scroll = QScrollArea()
        cards_widget = QWidget()
        cards_layout = QVBoxLayout()
        for product in fetch_products():
            card = ProductCard(product)
            cards_layout.addWidget(card)
        cards_widget.setLayout(cards_layout)
        scroll.setWidget(cards_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
