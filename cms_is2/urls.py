
from django.contrib import admin
from django.urls import path, re_path, include
from app.views import resultados_busqueda,PaginaNoEncontradaView
from django.conf import settings
from django.conf.urls.static import static
from contenido import views
from app import views
from accounts import views
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ckeditor_views

urlpatterns = [
    path('ckeditor/upload/',login_required(ckeditor_views.upload), name='ckeditor_upload'),
    path('ckeditor/browse/',never_cache(ckeditor_views.browse), name='ckeditor_browse'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('contenido/', include('contenido.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('buscar/', resultados_busqueda, name='resultados_busqueda'),
    re_path(r'^comments/', include('django_comments_xtd.urls')),
    re_path(r'^.*/$', PaginaNoEncontradaView.as_view(), name='pagina_no_encontrada'),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
