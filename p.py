import sys  # Для управления приложением
import psycopg2  # Для подключения к PostgreSQL
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem

# Параметры подключения к БД
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'dbname': 'postgres',   # Имя базы данных
    'user': 'postgres',         # Логин
    'password': '12345678' # Пароль (замени на свой)
}


# Функция для получения данных из БД
def get_products():
    conn = psycopg2.connect(**DB_CONFIG)  # Подключаемся к БД
    cursor = conn.cursor()                # Создаём курсор (для выполнения запросов)

    query = """
        SELECT
            pt.product_type,
            p.product_name,
            p.articul,
            p.min_cost_for_partner,
            mt.material_type,
            ROUND(SUM(pw.time_todo)) AS manufacture_time
        FROM products p
        JOIN product_types pt ON p.product_type_id = pt.product_type_id
        JOIN material_types mt ON p.material_type_id = mt.material_type_id
        LEFT JOIN product_workshops pw ON p.product_id = pw.product_id
        GROUP BY pt.product_type, p.product_name, p.articul, p.min_cost_for_partner, mt.material_type
    """  # SQL-запрос (объяснён выше)

    cursor.execute(query)         # Выполняем запрос
    products = cursor.fetchall()  # Получаем все строки с данными
    cursor.close()                # Закрываем курсор
    conn.close()                  # Закрываем подключение
    return products               # Возвращаем список продуктов

# Окно программы
class ProductViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Продукция компании")  # Заголовок окна
        self.setGeometry(100, 100, 600, 400)       # Размер окна

        layout = QVBoxLayout()           # Вертикальное расположение
        self.product_list = QListWidget()  # Список для вывода продукции
        layout.addWidget(self.product_list)
        self.setLayout(layout)

        self.load_products()  # Загрузка данных при старте

    # Метод загрузки данных
    def load_products(self):
        products = get_products()  # Получили данные из БД
        for product in products:
            # Распаковываем каждое поле
            type_, name, article, min_price, material, time = product

            # Формируем текст для отображения
            item_text = (
                f"Тип: {type_} | {name}\n"
                f"Арт: {article}\n"
                f"Мин. цена: {min_price} ₽\n"
                f"Материал: {material}\n"
                f"Время изготовления: {time} часов"
            )

            # Добавляем в список
            item = QListWidgetItem(item_text)
            self.product_list.addItem(item)


# Запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)   # Создаём приложение
    viewer = ProductViewer()       # Создаём окно
    viewer.show()                  # Показываем
    sys.exit(app.exec_())          # Выход при закрытии
