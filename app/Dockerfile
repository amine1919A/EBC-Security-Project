FROM php:8.2-fpm

RUN apt-get update && apt-get install -y \
    git unzip libpq-dev libzip-dev libicu-dev libpng-dev libjpeg-dev curl \
    --no-install-recommends \
    && docker-php-ext-install pdo pdo_mysql zip intl gd opcache

RUN curl -sS https://getcomposer.org/installer | php \
    && mv composer.phar /usr/local/bin/composer

WORKDIR /var/www/html

COPY symfony/composer.json symfony/composer.lock* ./
RUN composer install --no-dev --no-interaction --no-progress --optimize-autoloader

COPY symfony/ .

RUN mkdir -p var && chown -R www-data:www-data var/ public/

STOPSIGNAL SIGQUIT
