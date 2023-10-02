contenido package
=================

contenido.forms module
----------------------

Formularios de Contenido
~~~~~~~~~~~~~~~~~~~~~~~~

La clase ``ContenidoForm`` importa una libreria llamada ``CKEditorWidget`` que nos permite utilizar texto enriquecido.

La clase ``CategoriaForm`` forumalio para la creacion de categoria.

La clase ``CategoriaEditForm``  formulario para la edicion de categoria.

.. automodule:: contenido.forms
   :members:
   :undoc-members:
   :show-inheritance:


contenido.models module
-----------------------

Modelos de Contenido
~~~~~~~~~~~~~~~~~~~~

La clase ``Cotenido`` importa RichTextField de CKEditorWidget para el texto enriquecido.

La clase ``Categoria`` posee un campo de moderacion.

La clase ``VersionContenido`` es un modelo para realizar un historial de cambios(versiones) del contenido.

.. automodule:: contenido.models
   :members:
   :undoc-members:
   :show-inheritance:

contenido.urls module
---------------------

Urls de Contenido
~~~~~~~~~~~~~~~~~

::

   urlpatterns = [
      path('crear', login_required(views.ContenidoFormView.as_view()) , name='contenido-crear'),
      path('version', login_required(views.ContenidoVersionListView.as_view()) , name='contenido-version'),
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

      path('contenido/<int:pk>/editar/', views.EditarContenidoView.as_view(), name='editar-contenido'),

      path('autor/<int:pk>/', views.detalle_autor, name='detalle_autor'),

      path('kanban/', views.kanban_view, name='kanban'),

      path('borrador/<int:pk>/editar/', views.EditarBorradorView.as_view(), name='editar-borrador'),
      path('version/<int:version_id>/editar/', views.editar_version, name='editar-version'),
   ]


contenido.views module
----------------------

Vistas de Contenido
~~~~~~~~~~~~~~~~~~~

La clase ``ContenidoFormView`` es la vista del contenido con texto enriquecido.

La clase ``CategoriaFormView`` es la vista de la categoria con o sin moderacion.

La clase ``CategoriaListView`` es la vista de las categorias ya creadas.

La clase ``CategoriaDetailView`` es la vista de los detalles de la categoria.

La clase ``CategoriaUpdateView`` es la vista para la actualizacion de las categorias.

La clase ``DesactivarCategoriaView`` sirve para dar de baja una categoria.

La clase ``ActivarCategoriaView`` sirve para reactivar una categoria.

La clase ``MostrarContenidosView`` es la vista para mostrar los contenidos. 

La clase ``ListarRevisionesView`` es la vista para mostrar los contenidos en revision.

La funcion ``publicar_contenido`` 

.. automodule:: contenido.views
   :members:
   :undoc-members:
   :show-inheritance:



.. automodule:: contenido
   :members:
   :undoc-members:
   :show-inheritance:
