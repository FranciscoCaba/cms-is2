#!/bin/bash

# Variables
db_name="cms_prod"
db_user="cmsadmin"
db_password="cmsadmin"

mkdir ../static
mkdir ../staticfiles

# Requisitos del sistema
sudo apt update -y
sudo apt install python3 python3-venv libpq-dev postgresql postgresql-contrib nginx curl -y

# Nginx al firewall
sudo ufw allow 'Nginx Full'

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

# A la carpeta del proyecto
cd ..

# Migraciones, semilla y archivos estaticos
python manage.py makemigrations --settings=cms_is2.produccion
python manage.py migrate --settings=cms_is2.produccion
python manage.py semilla --settings=cms_is2.produccion
python manage.py collectstatic --noinput --settings=cms_is2.produccion

# Abrirmos el firewall para el puerto 8000
sudo ufw allow 8000

echo 'Desactivando el entorno virtual...'
deactivate

# Volvemos al directorio deploy
cd ./deploy/

# Copia de archivos de configuracion gunicorn
sudo cp 'gunicorn.socket' 'etc/systemd/system/'
sudo cp 'gunicorn.service' 'etc/systemd/system/'

# Activamos el servicio
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

# Configuracion de nginx
sudo cp 'cms' '/etc/nginx/sites-available/'
sudo ln -s /etc/nginx/sites-available/cms /etc/nginx/sites-enabled/

# Reiniciamos nginx
sudo systemctl restart nginx
