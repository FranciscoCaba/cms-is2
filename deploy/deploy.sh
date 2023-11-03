#!/bin/bash

# Variables
db_name="cms"
db_user="cmsadmin"
db_password="cmsadmin"

mkdir ../static
mkdir ../staticfiles

# Requisitos del sistema
sudo apt update -y
sudo apt install python3 python3-venv libpq-dev postgresql postgresql-contrib nginx curl -y

# Ejecutar los comandos con sudo su postgres
sudo su postgres <<EOF
psql -c "CREATE DATABASE $db_name;"
psql -c "CREATE USER $db_user WITH PASSWORD '$db_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE $db_name TO $db_user;"
EOF

echo 'Creando el entorno virtual...'
python3 -m venv ../../venv

echo 'Activando el entorno virtual...'
source ../../venv/bin/activate

echo 'Instalando dependencias...'
pip install -r '../requirements.txt'

cd ..
python manage.py migrate --settings=cms_is2.produccion
python manage.py collectstatic --noinput --settings=cms_is2.produccion

echo 'Desactivando el entorno virtual...'
deactivate



