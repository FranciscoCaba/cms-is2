
from django.contrib import admin
from django.urls import path, re_path, include
from app.views import buscar_contenido, resultados_busqueda,PaginaNoEncontradaView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('contenido/', include('contenido.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('buscar/', buscar_contenido, name='buscar_contenido'),
    path('resultados_busqueda/', resultados_busqueda, name='resultados_busqueda'),
    re_path(r'^.*/$', PaginaNoEncontradaView.as_view(), name='pagina_no_encontrada'),
]
