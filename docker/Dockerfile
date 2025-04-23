# Используем официальный PHP-FPM образ (версия можно менять по необходимости)
FROM php:8.2-fpm

# Обновляем систему и устанавливаем необходимые системные библиотеки
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    unzip \
    curl \
    && docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

WORKDIR /var/www/html

EXPOSE 9000

# Запуск PHP-FPM
CMD ["php-fpm"]

