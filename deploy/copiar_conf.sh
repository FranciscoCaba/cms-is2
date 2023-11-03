#!/bin/bash

# Copia de archivos de configuracion gunicorn
sudo cp 'gunicorn.socket' '/etc/systemd/system/'
sudo cp 'gunicorn.service' '/etc/systemd/system/'

# Activamos el servicio
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

# Configuracion de nginx
sudo cp 'cms' '/etc/nginx/sites-available/'
sudo ln -s /etc/nginx/sites-available/cms /etc/nginx/sites-enabled/

# Reiniciamos nginx
sudo systemctl restart nginx

# Nginx al firewall
sudo ufw allow 'Nginx Full'

