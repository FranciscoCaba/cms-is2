# Proyecto-cms-is2-eq01
## Integrantes
 - Osmani Jose Mestre Riveros
 - Francisco Daniel Cabañas Corvalán
 - Tobías Daniel Otazo Wiegert
 - Derlis Ariel Cáceres Núñez

## Requisitos
 - Python==3.11
 - PostgreSql 15:

Y ejecutando el comando  " pip install -r requirements.txt " estaremos instalando
 - django==4.2.4
 - whitenoise==6.5.0
 - psycopg2-binary==2.9.7
 - crispy-bootstrap5==0.7
 - Sphinx==7.2.4
 - sphinx_rtd_theme==1.3.0
 - django-ckeditor==6.7.0
 - lorem
 - gunicorn
 - django-cloudinary-storage==0.3.0
 - cloudinary==1.35.0
 - python-decouple==3.8
 - python-magic==0.4.27
 - django-storages==1.14
 - Pillow==9.0.1
 
que tambien son requisitos para poder correr correctamente el proyecto

## Ejecucion Del Proyecto
Primero y antes que nada es necesario tener correctamente configurado su SGBD (sistema gerenciador de base de datos) con las bases de datos creadas
y luego configurar los archivos settings.py, desarrollo.py y produccion.py.

En settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cms_dev', #Aqui configurar el nombre de la base de datos para desarrollo
        'USER': 'postgres', #Configurar con nombre del user que se esta utilizando
        'PASSWORD': 'postgres', #Colocar la contrasenia que se sta utilizando
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

En desarrollo.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cms_dev', #Aqui configurar el nombre de la base de datos para desarrollo
        'USER': 'postgres', #Configurar con nombre del user que se esta utilizando
        'PASSWORD': 'postgres', #Colocar la contrasenia que se sta utilizando
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

En produccion.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cms', #Aqui configurar el nombre de la base de datos para desarrollo
        'USER': 'postgres', #Configurar con nombre del user que se esta utilizando
        'PASSWORD': 'postgres', #Colocar la contrasenia que se sta utilizando
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Para ejecutar el programa se debe ejecutar desde el directorio " cms-is2 " una serie de comandos:
 - python3 manage.py makemigrations
 - python3 manage.py migrate
 - python3 manage.py runserver 

Posteriormente dar ctrl click a la direccion de ip localhost que se provee al ejecutar el comando.

### Para ejecutar pruebas unitarios del codigo se debe desde el directorio "cms-is2 " ejecutar el comando:
 - python3 manage.py test .tests_....py

Para elejir que test usamos simplemente en la parte de .test_....py escribimos el test que deseamos realizar por ej:
 - python3 manage.py test .tests_usuario.py

### Para ejecutar la documentacion del codigo se debe desde el directorio " cms-is2/docs/_build/html/ " ejecutar el comando:
 - python3 -m http.server 8001

Posteriormente dar ctrl click a la direccion ip de localhost que se provee al ejecutar el comando.

