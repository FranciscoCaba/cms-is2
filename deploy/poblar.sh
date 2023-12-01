#!/bin/bash

#Volvemos un directorio atras
cd ..

# Comandos django para inicializar el proyecto
python manage.py migrate --settings=cms_is2.produccion
python manage.py semilla --settings=cms_is2.produccion
python manage.py collectstatic --noinput --settings=cms_is2.produccion

