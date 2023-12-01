#!/bin/bash

# Variables
db_name="cms_dev"

# Habilitamos el puerto 8000
sudo ufw allow 8000

mkdir static
mkdir staticfiles

# Requisitos del sistema
sudo apt update -y
sudo apt install python3 python3-venv libpq-dev postgresql postgresql-contrib nginx curl -y

sudo su postgres <<EOF
psql -c "CREATE DATABASE $db_name;"
psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"
EOF

# Se crea el entorno virtual
python3 -m venv ./../venv

# Se activa el entorno virtual
source ../venv/bin/activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py semilla
python manage.py collectstatic --noinput

# Ejecutamos el servidor
python manage.py runserver
