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

