FROM php:8.2-fpm as builder

RUN apt-get update && apt-get install -y \
    git unzip libpq-dev libzip-dev libicu-dev libpng-dev libjpeg-dev \
    --no-install-recommends \
    && docker-php-ext-install pdo pdo_mysql zip intl gd opcache \
    && pecl install apcu \
    && docker-php-ext-enable apcu

COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

COPY symfony/composer.json symfony/composer.lock* ./
RUN composer install --no-dev --no-interaction --no-progress --optimize-autoloader 2>/dev/null || true

COPY symfony/ .
RUN composer dump-autoload --optimize

RUN mkdir -p var && chown -R www-data:www-data var/ public/

FROM php:8.2-fpm

RUN apt-get update && apt-get install -y \
    libpq-dev libzip-dev libicu-dev \
    --no-install-recommends \
    && docker-php-ext-install pdo pdo_mysql zip intl gd opcache \
    && pecl install apcu \
    && docker-php-ext-enable apcu

COPY --from=builder /var/www/html /var/www/html

WORKDIR /var/www/html

STOPSIGNAL SIGQUIT
