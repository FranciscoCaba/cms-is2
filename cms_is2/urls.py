
from django.contrib import admin
from django.urls import path, re_path, include
from app.views import PaginaNoEncontradaView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('contenido/', include('contenido.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^.*/$', PaginaNoEncontradaView.as_view(), name='pagina_no_encontrada'),
]
