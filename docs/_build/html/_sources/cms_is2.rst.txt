cms\_is2 package
================
Urls del Proyecto
~~~~~~~~~~~~~~~~~

::
   
   urlpatterns = [
      path('ckeditor/upload/',login_required(ckeditor_views.upload), name='ckeditor_upload'),
      path('ckeditor/browse/',never_cache(ckeditor_views.browse), name='ckeditor_browse'),
      path('ckeditor/', include('ckeditor_uploader.urls')),
      path('admin/', admin.site.urls),
      path('', include('app.urls')),
      path('contenido/', include('contenido.urls')),
      path('accounts/', include('django.contrib.auth.urls')),
      re_path(r'^.*/$', PaginaNoEncontradaView.as_view(), name='pagina_no_encontrada'),
   ] 
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


Configuraciones Del proyecto
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   from pathlib import Path
   import os
   from decouple import config
   # Build paths inside the project like this: BASE_DIR / 'subdir'.
   BASE_DIR = Path(__file__).resolve().parent.parent
   
   SECRET_KEY = 'django-insecure-3@83r2(*0+$g332h5y^sdsjazqu&ovuea^_w^3-=bl@^!&4#$)'

   DEBUG = True
   
   ALLOWED_HOSTS = ['localhost', 'cms.local', '127.0.0.1']

::

   INSTALLED_APPS = [
      'crispy_forms',
      'crispy_bootstrap5',
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      'cloudinary_storage',
      'cloudinary',
      'accounts.apps.AccountsConfig',
      'app',
      'contenido',
      'ckeditor',
      'storages',
      'ckeditor_uploader',
   ]

Lineas necesarias para que funcione la libreria que se encarga de formatear 
los formularios::

   CRISPY_ALLOWED_TEMPLATE_PACK = 'bootstrap5'
   CRISPY_TEMPLATE_PACK = 'bootstrap5'

El whitenoise es una libreria de django para servir archivos estaticos
ya que por defecto django no se encarga de servir archivos estaticos 
en produccion y tiene que ser declarado por debajo del middleware de
seguridad de django ya que trabaja en conjunto con el::
   
   MIDDLEWARE = [
      'django.middleware.security.SecurityMiddleware',
      'whitenoise.middleware.WhiteNoiseMiddleware',
      'django.contrib.sessions.middleware.SessionMiddleware',
      'django.middleware.common.CommonMiddleware',
      'django.middleware.csrf.CsrfViewMiddleware',
      'django.contrib.auth.middleware.AuthenticationMiddleware',
      'django.contrib.messages.middleware.MessageMiddleware',
      'django.middleware.clickjacking.XFrameOptionsMiddleware',
   ]

Aqui van las urls del proyecto::

   ROOT_URLCONF = 'cms_is2.urls'

::

   TEMPLATES = [
      {
         'BACKEND': 'django.template.backends.django.DjangoTemplates',
         'DIRS': [],
         'APP_DIRS': True,
         'OPTIONS': {
               'context_processors': [
                  'django.template.context_processors.debug',
                  'django.template.context_processors.request',
                  'django.contrib.auth.context_processors.auth',
                  'django.contrib.messages.context_processors.messages',
               ],
         },
      },
   ]

Declara la ubic del modulo para la conexion con apache::

   WSGI_APPLICATION = 'cms_is2.wsgi.application'

Contrasenas sin requisitos son posibles gracias al::

   AUTH_PASSWORD_VALIDATORS = []

Cambia el idioma de componentes traducibles del proyecto::

   LANGUAGE_CODE = 'es-es'

::

   TIME_ZONE = 'UTC'

   USE_I18N = True

   USE_TZ = True

Direccion y ruta de archivos estaticos para servir con whitenoise::

   STATIC_URL = 'static/'
   STATIC_ROOT = BASE_DIR / "staticfiles"
   STATICFILES_DIRS = [
      os.path.join(BASE_DIR, "static")
   ] 

   STORAGES = {
      "default": {
         "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
         "OPTIONS": {  
               
         },
      },  
      "staticfiles": {
         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
      },
   }
   CLOUDINARY_STORAGE = {
      'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
      'API_KEY': config('CLOUDINARY_API_KEY'),
      'API_SECRET': config('CLOUDINARY_API_SECRET'),
   }

Direccion y ruta de archivos de media::

   MEDIA_URL = 'media/'
   MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

   DEBUG = True

::

   DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

VARIABLES DE REDIRECCION EN LOGIN Y LOGOUT::

   LOGIN_REDIRECT_URL = 'index'
   LOGOUT_REDIRECT_URL = 'index'

Configuracion para la conexion con la base de datos::
   
   DATABASES = {
      'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'cms_dev',
         'USER': 'postgres',
         'PASSWORD': 'postgres',
         'HOST': 'localhost',
         'PORT': '5432',
      }
   }
