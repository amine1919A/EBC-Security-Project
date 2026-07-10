FROM php:8.2-fpm

# Installation de l'agent Contrast (PHP)
# Note: Télécharger l'agent depuis https://app.contrastsecurity.com
# Remplacer <TEAM_SERVER_URL> et <AGENT_NAME> par les valeurs du compte

RUN apt-get update && apt-get install -y wget unzip \
    && docker-php-ext-install pdo pdo_mysql

# Copier l'agent Contrast (à télécharger manuellement)
# COPY contrast-php-agent.so /usr/local/lib/php/extensions/no-debug-non-zts-20220829/
# COPY contrast-php.ini /usr/local/etc/php/conf.d/99-contrast.ini

# Alternative: Agent en mode sidecar (recommandé pour Docker)
EXPOSE 9010
