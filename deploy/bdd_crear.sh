#!/bin/bash

# Variables
db_name="cms_prod"
db_user="cmsadmin"
db_password="cmsadmin"

sudo su postgres <<EOF
echo 'Creando base de datos $db_name ...'
psql -c "CREATE DATABASE $db_name;"

echo 'Creando usuario $db_user con contrasenha $db_password ...'
psql -c "CREATE USER $db_user WITH PASSWORD '$db_password';"

echo 'Dando privilegios al usuario sobre la base de datos...'
psql -c "GRANT ALL PRIVILEGES ON DATABASE $db_name TO $db_user;"
EOF
