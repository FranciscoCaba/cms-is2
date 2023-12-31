from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
urlpatterns = [
    path('crear', login_required(views.ContenidoFormView.as_view()) , name='contenido-crear'),
    path('version', login_required(views.ContenidoVersionListView.as_view()) , name='contenido-version'),
    path('version/<int:contenido_id>/', login_required(views.ContenidoVersionListView.as_view()) , name='contenido-version'),
    path('historial', login_required(views.ContenidoHistorialListView.as_view()) , name='contenido-historial'),
    path('categoria/crear', login_required(views.CategoriaFormView.as_view()), name='categoria-crear'),
    path('categoria', views.CategoriaListView.as_view(), name='categoria-list'),
    path('categoria/<int:pk>/', views.CategoriaDetailView.as_view(), name='categoria-detail'),
    path('categoria/<int:pk>/update/', views.CategoriaUpdateView.as_view(), name='categoria-update'),
    path('categoria/<int:pk>/desactivar', views.DesactivarCategoriaView.as_view(), name='desactivar-categoria'),
    path('categoria/<int:pk>/activar', views.ActivarCategoriaView.as_view(), name='activar-categoria'),
    path('categoria/<int:pk>/listar', views.MostrarContenidosView.as_view(), name='mostrar_contenidos'),
    
    path('publicar/',views.ContenidosApublicarView.as_view(),name= 'list_a_publicar'),
    path('publicar/<int:pk>/', views.apublicar_contenido, name='a-publicar'),
    path('publicar/ver/<int:pk>/', views.UnContenidoApublicarView.as_view(), name='list_un_a_publicar'),
    path('revision/', views.ListarRevisionesView.as_view(), name='listar_revisiones'),
    path('revision/ver/<int:pk>/', views.ListarUnaRevisionView.as_view(), name='listar_una_revision'),
    path('contenido/<int:pk>/publicar/', views.publicar_contenido, name='publicar_contenido'),
    path('contenido/<int:pk>/rechazar/', views.rechazar_contenido, name='rechazar_contenido'),

    path('borradores/', views.ContenidoBorradorListView.as_view(), name='borradores_lista'),
    path('rechazados/', views.ContenidoRechazadoListView.as_view(), name='rechazados_lista'),

    path('contenido/<int:contenido_id>/toggle-like/', views.toggle_like, name='toggle_like'),
    path('contenido/<int:contenido_id>/toggle-dislike/', views.toggle_dislike, name='toggle_dislike'),
    path('contenido/<int:pk>/', views.detalle_contenido, name='detalle_contenido'),
    path('contenido/<int:categoria_id>/toggle-favorito/', views.toggle_favorito, name='toggle_favorito'),
    path('contenido/<int:contenido_id>/compartir/', views.compartir_contenido, name='compartir_contenido'),
    path('contenido/<int:pk>/desactivar/', views.confirmar_desactivacion, name='confirmar_desactivacion'),
    path('contenido/<int:pk>/destacar/', views.destacar_contenido, name='destacar_contenido'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),

    path('contenido/<int:pk>/editar/', views.EditarContenidoView.as_view(), name='editar-contenido'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('delete_video/<int:video_id>/', views.delete_video, name='delete_video'),
    path('delete_archivo/<int:archivo_id>/', views.delete_archivo, name='delete_archivo'),

    path('autor/<int:pk>/', views.detalle_autor, name='detalle_autor'),

    path('kanban/', views.kanban_view, name='kanban'),
    path('kanban/all/', views.all_kanban_view, name='all_kanban'),

    path('borrador/<int:pk>/editar/', views.EditarBorradorView.as_view(), name='editar-borrador'),
    path('version/<int:version_id>/editar/', views.editar_version, name='editar-version'),
    path('historial/<int:version_id>/', views.detalle_historial, name='detalle-historial'),
    path('rechazado/<int:pk>/editar/', views.EditarRechazadoView.as_view(), name='editar-rechazado'),

    path('qr_code/', views.generate_qr_code, name='generate_qr_code'),

    path('error/', views.error403, name='error403'),

    path('megusta/', views.megusta, name='megusta'),
    path('seguidos/', views.seguidos, name='seguidos'),
]
