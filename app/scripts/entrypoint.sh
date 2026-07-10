#!/bin/sh
set -e

echo "🚀 Démarrage de l'application EBC..."

# Attendre MySQL
echo "⏳ Attente de MySQL..."
until php -r "new PDO('mysql:host=mysql;dbname=ebc_sulu', 'ebc_user', 'ebc_pass_2024');" 2>/dev/null; do
    sleep 2
done
echo "✅ MySQL prêt"

# Migrations si applicable
if [ -f bin/console ]; then
    php bin/console doctrine:migrations:migrate --no-interaction 2>/dev/null || true
fi

# Démarrage PHP-FPM
echo "✅ Application prête sur http://0.0.0.0:9000"
php-fpm
