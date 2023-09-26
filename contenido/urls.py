from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
urlpatterns = [
    path('crear', login_required(views.ContenidoFormView.as_view()) , name='contenido-crear'),
    path('categoria/crear', login_required(views.CategoriaFormView.as_view()), name='categoria-crear'),
    path('categoria', views.CategoriaListView.as_view(), name='categoria-list'),
    path('categoria/<int:pk>/', views.CategoriaDetailView.as_view(), name='categoria-detail'),
    path('categoria/<int:pk>/update/', views.CategoriaUpdateView.as_view(), name='categoria-update'),
    path('categoria/<int:pk>/desactivar', views.DesactivarCategoriaView.as_view(), name='desactivar-categoria'),
    path('categoria/<int:pk>/activar', views.ActivarCategoriaView.as_view(), name='activar-categoria'),
    path('categoria/<int:pk>/listar', views.MostrarContenidosView.as_view(), name='mostrar_contenidos'),
    
    path('revision/', views.ListarRevisionesView.as_view(), name='revisar'),
    path('contenido/<int:pk>/publicar/', views.publicar_contenido, name='publicar_contenido'),
    path('contenido/<int:pk>/rechazar/', views.rechazar_contenido, name='rechazar_contenido'),

    path('borradores/', views.ContenidoBorradorListView.as_view(), name='borradores_lista'),
    path('rechazados/', views.ContenidoRechazadoListView.as_view(), name='rechazados_lista'),

    path('contenido/<int:contenido_id>/toggle-like/', views.toggle_like, name='toggle_like'),
    path('contenido/<int:pk>/', views.detalle_contenido, name='detalle_contenido'),

    path('contenido/<int:pk>/editar/', views.EditarContenidoView.as_view(), name='editar-contenido')
]
