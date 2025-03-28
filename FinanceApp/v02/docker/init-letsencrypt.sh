#!/bin/bash

domains=(wedos.cz www.wedos.cz)
email="" # Změňte na váš email
staging=0 # Nastavte na 1 pro staging prostředí

# Vytvoření adresářů pro certbot
mkdir -p certbot/conf certbot/www

# Vytvoření dummy certifikátu pro první spuštění
docker-compose run --rm --entrypoint "\
  openssl req -x509 -nodes -newkey rsa:2048 -days 1\
    -keyout '/etc/letsencrypt/live/wedos.cz/privkey.pem' \
    -out '/etc/letsencrypt/live/wedos.cz/fullchain.pem' \
    -subj '/CN=localhost'" certbot

# Spuštění nginx
docker-compose up --force-recreate -d nginx

# Smazání dummy certifikátu
docker-compose run --rm --entrypoint "\
  rm -Rf /etc/letsencrypt/live && \
  rm -Rf /etc/letsencrypt/archive && \
  rm -Rf /etc/letsencrypt/renewal" certbot

# Požádání o certifikát
docker-compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    $staging_arg \
    --email $email \
    -d ${domains[0]} \
    -d ${domains[1]} \
    --rsa-key-size 4096 \
    --agree-tos \
    --force-renewal" certbot

# Restart nginx
docker-compose up -d nginx 