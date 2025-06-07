жопа 
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
ROUND(AVG(pw.time_todo)) AS avg_time
📘 AVG() — среднее по значению (например, среднее время изготовления в разных цехах)

✅ 2. Максимальное / минимальное время
MAX(pw.time_todo) AS max_time,
MIN(pw.time_todo) AS min_time
✅ 3. Количество задействованных цехов
COUNT(pw.workshop_id) AS workshops_count
Подсчитывает, в скольких цехах участвует производство товара

✅ 4. Фильтрация по типу продукта
WHERE pt.product_type = 'Стол'
✅ 5. Фильтрация по цене
WHERE p.min_cost_for_partner > 3000
Можно комбинировать:
WHERE pt.product_type = 'Шкаф' AND p.min_cost_for_partner < 5000
✅ 6. Умножение и деление
(p.min_cost_for_partner * 1.2) AS cost_with_markup,
(p.min_cost_for_partner / 100) AS price_in_hundreds
Можно делить, умножать, складывать и вычитать прямо в SELECT

✅ 7. Сумма нескольких чисел
Допустим, у тебя есть length, width, height, и ты хочешь их сложить:
(p.length + p.width + p.height) AS dimensions_sum
Или, например, найти объём:

(p.length * p.width * p.height) AS volume
✅ 8. Группировка только по типу и материалу
Если не нужны названия и артикулы:
GROUP BY pt.product_type, mt.material_type
Тогда получишь обобщённую статистику: например, "все столы из ДСП — 20 часов".

✅ 9. Сортировка результатов
ORDER BY manufacture_time DESC  -- по убыванию
ORDER BY min_cost_for_partner ASC -- по возрастанию цены
✅ 10. Ограничение количества строк
LIMIT 10
🧠 Комбинируй:
Например, показать только столы, у которых цена > 3000 и отсортировать по времени:
SELECT ...
FROM ...
WHERE pt.product_type = 'Стол' AND p.min_cost_for_partner > 3000
GROUP BY ...
ORDER BY manufacture_time DESC
LIMIT 5;

sql скрипт пример

SELECT 
    partners.partner_name,           -- имя партнёра
    partners.director_name,          -- имя директора партнёра
    partners.partner_phone,          -- телефон
    partners.rating,                 -- рейтинг
    sales_summary.total_sales,       -- общая сумма продаж
    partners_types.type_name,        -- тип партнёра (например, оптовик, розничный и т.д.)
 CASE
        WHEN total_sales <= 10000 THEN 0
        WHEN total_sales > 10000 AND total_sales <= 50000 THEN 5
        WHEN total_sales > 50000 AND total_sales <= 300000 THEN 10
        ELSE 15
    END AS discount
FROM (
    SELECT 
        id_partner, 
        SUM(product_amount) AS total_sales
    FROM 
        partner_products
    GROUP BY 
        id_partner
    ORDER BY 
        id_partner
) AS sales_summary

Что делает:

Из таблицы partner_products собирается:

id_partner — идентификатор партнёра

SUM(product_amount) — суммируются все продажи (например, количество или сумма продукции)

Это сгруппировано по каждому партнёру → получается таблица sales_summary, где для каждого партнёра указана общая сумма продаж (total_sales)

JOIN partners ON sales_summary.id_partner = partners.id
JOIN partners_types ON partners.id_type_partner = partners_types.id;
Что делает:

Присоединяет таблицу partners:

по ключу id_partner из sales_summary и id из partners

Присоединяет таблицу partners_types:

по id_type_partner из partners и id из partners_types

есть, победа
ВАПВЩПРВАПЩВПВПВПВ
![image](https://github.com/user-attachments/assets/55bdc60a-5113-46d2-b69b-42d0911b3ac8)
 СКУЛЬ СКРИПТ

есть, победа
  ща потом скрипт бахну, пока объяняют задание то кторе я тебе скидывал

прям одинв один задание лол

если чо пиши, я каждые 5 мин обновляю страницу и на перерыве приходи


вот скриптик

CREATE TABLE material_types (
	id SERIAL PRIMARY KEY,
	material_type VARCHAR(100),
	percent_of_loss NUMERIC(4,2),
);

CREATE TABLE product_types (
	id SERIAL PRIMARY KEY,
	product_type VARCHAR(100),
	koef_product_type NUMERIC(4,2)
);

CREATE TABLE products(
	id SERIAL PRIMARY KEY,
	product_type_id INT REFERENCES product_types(id),
	product_name VARCHAR(200),
	articul INTEGER,
	minimal_cost_for_partner NUMERIC(10,2),
	roll_width NUMERIC (4,2)
);

CREATE TABLE materials (
	id SERIAL PRIMARY KEY,
	material_name VARCHAR(200),
	material_type_id INT REFERENCES material_types(id),
	price_per_unit_of_material NUMERIC(10,2),
	quantity_in_stock NUMERIC(10,2),
	min_quantity (10,2),
	quantity_per_package INTEGER,
	unit_of_measurement VARCHAR(100)
);

CREATE TABLE product_materials(
	product_id INT REFERENCES products(id),
	material_id INT REFERENCES materials(id),
	required_amount_of_material NUMERIC(4,2)
);

unit_of_measurement VARCHAR(100) по идеи для этого надо отдельную сделать, но сказали можно не делать



мне чото сделать с этим?

вспомни че я тебе в тг писал пхаахп, ну ваще было бы классно проверить лол. Ну и в зависмости от этого написать код, задание и пример интерфейса по идеи точно такое же, на перерыве сверим, но накидай лучше ща 
че нить



бля я думал ты уже закончил, уже 2 часа прошло

во финальный скрипт, скоро перерыв, увидимся

CREATE TABLE material_types (
	id SERIAL PRIMARY KEY,
	material_type VARCHAR(100),
	percent_of_loss NUMERIC(4,2)
);

CREATE TABLE product_types (
	id SERIAL PRIMARY KEY,
	product_type VARCHAR(100),
	koef_product_type NUMERIC(4,2)
);

CREATE TABLE products(
	id SERIAL PRIMARY KEY,
	product_type_id INT REFERENCES product_types(id),
	product_name VARCHAR(200),
	articul INTEGER,
	minimal_cost_for_partner NUMERIC(10,2),
	roll_width NUMERIC (4,2)
);

CREATE TABLE materials (
	id SERIAL PRIMARY KEY,
	material_name VARCHAR(200),
	material_type_id INT REFERENCES material_types(id),
	price_per_unit_of_material NUMERIC(10,2),
	quantity_in_stock NUMERIC(10,2),
	min_quantity NUMERIC(10,2),
	quantity_per_package INTEGER,
	unit_of_measurement VARCHAR(100)
);

CREATE TABLE product_materials(
	product_id INT REFERENCES products(id),
	material_id INT REFERENCES materials(id),
	required_amount_of_material NUMERIC(4,2)
);



ща я у себя тут установлю пайчарм и проверю и скину

а скрин интерфейса будет?

он точно такой же, как я тебе скидывал, прям авбсолютно. Задание Стоимость продукта посчитать исходя из используемых материалов

слыш тут 6 куте, и ругается

Traceback (most recent call last):
  File "/home/student2/pyqt_project/main.py", line 118, in <module>
    window = MainWindow()
             ^^^^^^^^^^^^
  File "/home/student2/pyqt_project/main.py", line 97, in __init__
    title.setFont(QFont('Arial', 14, QFont.bold()))
                                     ^^^^^^^^^^^^
TypeError: bold(self): first argument of unbound method must have type 'QFont' 




Вместо
python
title.setFont(QFont('Arial', 14, QFont.bold()))
нужно писать
python
title.setFont(QFont('Arial', 14, QFont.Weight.Bold))


напиши исправилось или нет

Да, но теперь это

  File "/home/student2/pyqt_project/main.py", line 96, in __init__
    title.setAlignment(Qt.AlignCenter)
                       ^^^^^^^^^^^^^^
AttributeError: type object 'Qt' has no attribute 'AlignCenter'





.setAlignment(Qt.AlignmentFlag.AlignCenter)
во на это измени и напиши получилось или еще ошибки
я создал тетс3.пай и он фул для 6 версии, напиши получилось или нет

победа чувак, спс

че тот же варик? 

крч отойду на 20-30 мин пока


ну вроде рабочий

да, всё норм)

А че скрипт подошел, который тут вначале в редми?)


ERROR: invalid input syntax for type integer: "20,8,2.7"
CONTEXT: COPY product_workshops, line 2, column product_id: "20,8,2.7"
загугли ошибку пж

братиш, постгрес не воспринимает запятые, и почему у тебя в id 2.7???? Ты походу напортачил с импортом таблиц, у тебя там нигде не должно быть запятых. Он же тебе говорит что ожидает число а ты ему 2.7. Ты ваще чет жестко в csv проеблася, ща у неиронки спрошу

С каким параметрами ты экспортируешь таблицы, а с какими импортируешь в постгресе?

у меня там нет заяптых файле, там с точками

Ну еще не должно быть запятых я имею ввиду, что они должны быть заменены на точки

Скинь скирны экспорта и импорта 

Бля ну если ваще хана будет, то раз уж варик я уже этот делал, я могу тебе свои csv загрузить, там потом подставишь их и скрипт, но это крайниый варик 

Ответ от неиронки

Ошибка invalid input syntax for type integer: "20,8,2.7" означает, что PostgreSQL пытается вставить значение "20,8,2.7" в столбец типа INTEGER, а это невозможно, потому что:

"20,8,2.7" — это строка, содержащая несколько чисел, разделённых запятыми.

Целое число (INTEGER) не может быть списком чисел или десятичным числом (например, 2.7 тоже невалидно для INTEGER).

Возможные причины
Неверный разделитель в CSV: скорее всего, вы используете запятую как разделитель значений, но ваши числовые значения тоже содержат запятые (возможно, в качестве десятичного разделителя — это часто бывает в русскоязычных Excel-файлах).

Неправильный формат числа: например, 2.7 — это число с плавающей точкой, а столбец product_id должен содержать целые числа (INTEGER).

Что делать
Проверьте CSV-файл, особенно строку 2, и убедитесь, что:

Столбец product_id содержит только целые числа: например, 20, 8, но не 2.7 или "20,8,2.7".

Разделитель столбцов — табуляция или точка с запятой, если в значениях встречаются запятые.

Пример корректной строки для COPY:

yaml
Копировать
Редактировать
20	1234	2024-01-01
Где:

20 — это product_id (целое число),

1234 — другой числовой столбец,

2024-01-01 — дата.

Как проверить и исправить
Если вы работаете с CSV:

Откройте его в текстовом редакторе или Excel.

Убедитесь, что:

Столбцы разделены корректно (например, точками с запятой, если в значениях есть запятые).

product_id содержит только одно целое число на строку.

Если вы пришлёте строку или файл CSV, вызвавший ошибку, я помогу точнее.





https://github.com/Xgimro/examH
вот тебе ссылка там скрипт и файлы, таблица продукт воркшопс

пхаха ребят, у вас экспорт таблицы не правильный, вы блять везде ставите ; а в продукт воркшопс в качестве разделителя ебашите запятые, ясен хуй он не подходит под ваши параметры импорта, либо в импорте поменяйте на запятые, либо в экспортируйте файлы их экселя с ;

 еще совет срезать заголовки, не обязательно, но говорят так правильно вроде. Тут уже сам решай 
