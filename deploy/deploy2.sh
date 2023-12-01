#!/bin/bash

# Variables
db_name="cms_prod"
db_user="cmsadmin"
db_password="cmsadmin"
workers=4

# Habilitamos el puerto 8000
sudo ufw allow 8000

mkdir static
mkdir staticfiles

# Requisitos del sistema
sudo apt update -y
sudo apt install python3 python3-venv libpq-dev postgresql postgresql-contrib nginx curl -y

sudo su postgres <<EOF
psql -c "CREATE DATABASE $db_name;"
psql -c "CREATE USER $db_user WITH PASSWORD '$db_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE $db_name TO $db_user;"
EOF

# Se crea el entorno virtual
python3 -m venv ../../venv

# Se activa el entorno virtual
source ../venv/bin/activate
pip install -r requirements.txt

python manage.py makemigrations --settings=cms_is2.produccion
python manage.py migrate --settings=cms_is2.produccion
python manage.py semilla --settings=cms_is2.produccion
python manage.py collectstatic --noinput --settings=cms_is2.produccion

## Configuracion de nginx
#sudo cp 'cms2' '/etc/nginx/sites-available/'
#sudo ln -s /etc/nginx/sites-available/cms /etc/nginx/sites-enabled/
#
## Reiniciamos nginx
#sudo systemctl restart nginx

# Ejecutamos el servidor
gunicorn --workers $workers --bind 0.0.0.0:8000 cms_is2.wsgi:application