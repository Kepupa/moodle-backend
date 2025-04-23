install: #установка зависимостей
		composer install

build: #сборка и подяние контенеров
	docker compose up -d --build

up: #поднятие контейнеров
	docker compose up -d

down: #опустить контейнеры
	docker compose down

check: #открыть lazydocker (можно посмотреть отсувствующие логи и другуйю информацию)
	lazydocker

rebuild: #пересборка контейнеров (сначала их опустит, а зачет занов сбилдит)
	docker cmopose down && docker compose up -d --build

laravel: #зайти внтуерь контейнера с laravel
	docker exec -it laravel bash

nginx: #зайти внутрь контейнера с nginx
	docker exec -it nginx sh

redis: #зайтит внутрь контейнера с redis
	docker exec -it redis bash

mysql: #зайти внткрь контейнера с mysql
	docker exec -it mysqlara bash

lint: #запустить codesniffer
	vendor/bin/phpcs

fix: #автофиксы
	vendor/bin/phpcbf

stan: # статический анализатор (php stan)
	vendor/bin/phpstan analyse

