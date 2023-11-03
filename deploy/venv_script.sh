#!/bin/bash

echo 'Creando el entorno virtual...'
python3 -m venv ../../venv

echo 'Activando el entorno virtual...'
source ../../venv/bin/activate

echo 'Instalando dependencias...'
pip install -r requirements.txt

echo 'Desactivando el entorno virtual...'
deactivate

