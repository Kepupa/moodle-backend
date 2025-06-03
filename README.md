Модуль 1
Удаляем столы, если они существуют
DROP TABLE IF EXISTS material_types CASCADE;
DROP TABLE IF EXISTS product_types CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS workshops CASCADE;
DROP TABLE IF EXISTS product_workshops CASCADE;


CREATE TABLE material_types (
  material_type_id SERIAL PRIMARY KEY UNIQUE, делаем ключ уникальный
  material_type VARCHAR(100) UNIQUE NOT NULL, варчар макс 100 символов
  percent_of_loss NUMERIC(4,2)  нумерик, (общее колво цифр, скок после запятой)
);

CREATE TABLE product_types (
  product_type_id SERIAL PRIMARY KEY UNIQUE,
  product_type VARCHAR(100) UNIQUE NOT NULL,
  coef_type_product NUMERIC(4,2)
);

CREATE TABLE products (
  product_id SERIAL PRIMARY KEY UNIQUE,
  product_type_id INT REFERENCES product_types(product_type_id), (ссылаемся на таблицу)
  product_name VARCHAR(100) UNIQUE NOT NULL,
  articul INTEGER UNIQUE NOT NULL,
  min_cost_for_partner NUMERIC(9,2),
  material_type_id INT REFERENCES material_types(material_type_id)
);

CREATE TABLE workshops (
  workshop_id SERIAL PRIMARY KEY UNIQUE,
  workshop_name VARCHAR(100) UNIQUE NOT NULL,
  workshop_type VARCHAR(100) NOT NULL,
  workshop_members INTEGER 
);

CREATE TABLE product_workshops(
  product_id INT REFERENCES products(product_id),
  workshop_id INT REFERENCES workshops(workshop_id),
  time_todo NUMERIC(2,2) NOT NULL
);

--------------------------
SELECT
    pt.product_type,
    p.product_name,
    p.articul,
    p.min_cost_for_partner,
    mt.material_type,
    ROUND(SUM(pw.time_todo)) AS manufacture_time
🔍 Что здесь происходит:
SELECT — говорим, какие поля мы хотим получить из таблиц.

pt.product_type — берём тип продукта из таблицы product_types.

p.product_name — название продукта из таблицы products.

p.articul — артикул.

p.min_cost_for_partner — минимальная цена для партнёра.

mt.material_type — тип материала, из таблицы material_types.

ROUND(SUM(pw.time_todo)) AS manufacture_time:

pw.time_todo — время, которое тратится в каждом цеху на изготовление этого продукта.

SUM(...) — суммируем общее время по всем цехам.

ROUND(...) — округляем полученное значение (если, например, получилось 2.67 → станет 3).

AS manufacture_time — даём этому столбцу новое имя: "время изготовления".

sql
FROM products p
🔍 Что это:
Таблица products — основная, от которой идём.

p — это псевдоним (alias), чтобы было короче писать, вместо products.product_name пишем p.product_name.

sql
JOIN product_types pt ON p.product_type_id = pt.product_type_id
🔍 Что это:
Соединяем таблицу products с таблицей product_types по полю product_type_id.

JOIN по умолчанию — это INNER JOIN, то есть выбираются только те продукты, у которых есть связанный тип.

pt — псевдоним для product_types.

sql
JOIN material_types mt ON p.material_type_id = mt.material_type_id
🔍 Что это:
Аналогично: присоединяем таблицу с типами материала (material_types) по ключу material_type_id.

sql
LEFT JOIN product_workshops pw ON p.product_id = pw.product_id
🔍 Что это:
LEFT JOIN — берём все продукты, даже если они не связаны с цехами.

Это важно, если есть продукты, которые ещё не распределены по цехам.

pw — псевдоним для product_workshops.

sql
GROUP BY pt.product_type, p.product_name, p.articul, p.min_cost_for_partner, mt.material_type
🔍 Что это:
Без GROUP BY ты не можешь использовать агрегатные функции (SUM, AVG, COUNT, и т.д.).

Поэтому мы группируем результат по всем полям, кроме того, по которому считаем SUM(...).

Почему все эти поля в GROUP BY?
SQL требует: всё, что не агрегируется (например, не SUM()), — должно быть в GROUP BY.

🧾 Результат запроса выглядит как таблица:
Тип продукта	Название	Артикул	Мин. цена	Материал	Время изготовления
Стол	Лофт 3	12345	3500.00	ДСП	4
Стул	Соло 1	33333	800.00	Фанера	2

✨ Подсказки:
Если хочешь считать среднее время изготовления, замени SUM(...) на AVG(...).

Если хочешь узнать сколько цехов участвуют — добавь COUNT(pw.workshop_id).

Можно добавить фильтр по типу продукта или цене через WHERE.

Варианты и замены:
✅ 1. Среднее время изготовления
sql
Копировать
Редактировать
ROUND(AVG(pw.time_todo)) AS avg_time
📘 AVG() — среднее по значению (например, среднее время изготовления в разных цехах)

✅ 2. Максимальное / минимальное время
sql
Копировать
Редактировать
MAX(pw.time_todo) AS max_time,
MIN(pw.time_todo) AS min_time
✅ 3. Количество задействованных цехов
sql
Копировать
Редактировать
COUNT(pw.workshop_id) AS workshops_count
Подсчитывает, в скольких цехах участвует производство товара

✅ 4. Фильтрация по типу продукта
sql
Копировать
Редактировать
WHERE pt.product_type = 'Стол'
✅ 5. Фильтрация по цене
sql
Копировать
Редактировать
WHERE p.min_cost_for_partner > 3000
Можно комбинировать:

sql
Копировать
Редактировать
WHERE pt.product_type = 'Шкаф' AND p.min_cost_for_partner < 5000
✅ 6. Умножение и деление
sql
Копировать
Редактировать
(p.min_cost_for_partner * 1.2) AS cost_with_markup,
(p.min_cost_for_partner / 100) AS price_in_hundreds
Можно делить, умножать, складывать и вычитать прямо в SELECT

✅ 7. Сумма нескольких чисел
Допустим, у тебя есть length, width, height, и ты хочешь их сложить:

sql
Копировать
Редактировать
(p.length + p.width + p.height) AS dimensions_sum
Или, например, найти объём:

sql
Копировать
Редактировать
(p.length * p.width * p.height) AS volume
✅ 8. Группировка только по типу и материалу
Если не нужны названия и артикулы:

sql
Копировать
Редактировать
GROUP BY pt.product_type, mt.material_type
Тогда получишь обобщённую статистику: например, "все столы из ДСП — 20 часов".

✅ 9. Сортировка результатов
sql
Копировать
Редактировать
ORDER BY manufacture_time DESC  -- по убыванию
ORDER BY min_cost_for_partner ASC -- по возрастанию цены
✅ 10. Ограничение количества строк
sql
Копировать
Редактировать
LIMIT 10
🧠 Комбинируй:
Например, показать только столы, у которых цена > 3000 и отсортировать по времени:

sql
Копировать
Редактировать
SELECT ...
FROM ...
WHERE pt.product_type = 'Стол' AND p.min_cost_for_partner > 3000
GROUP BY ...
ORDER BY manufacture_time DESC
LIMIT 5;








