#!/bin/bash

# Variables
db_name="cms_dev"
db_user="postgres"
db_password="postgres"

mkdir ../static
mkdir ../staticfiles

# Requisitos del sistema
sudo apt update -y
sudo apt install python3 python3-venv libpq-dev postgresql postgresql-contrib nginx curl -y

# Ejecutar los comandos con sudo su postgres
sudo su postgres <<EOF
psql -c "CREATE DATABASE $db_name;"
EOF

echo 'Creando el entorno virtual...'
python3 -m venv ../../venv

echo 'Activando el entorno virtual...'
source ../../venv/bin/activate

echo 'Instalando dependencias...'
pip install -r '../requirements.txt'

# A la carpeta del proyecto
cd ..
python manage.py migrate
python manage.py semilla
python manage.py collectstatic
python manage.py runserver

echo 'Desactivando el entorno virtual...'
deactivate
