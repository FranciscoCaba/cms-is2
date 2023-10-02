contenido package
=================

contenido.forms module
----------------------

Formularios de Contenido
~~~~~~~~~~~~~~~~~~~~~~~~

La clase ``ContenidoForm`` importa una libreria llamada ``CKEditorWidget`` que nos permite utilizar texto enriquecido.

La clase ``ContenidoEditForm`` es el formulario de la vista de edicion de contenido.

La clase ``CategoriaForm`` forumalio para la creacion de categoria.

La clase ``CategoriaEditForm``  formulario para la edicion de categoria.

La clase ``BorradorEditForm`` es el formulario de edicion de borrador de contenido.

La clase ``VersionContenidoEditForm`` es el formulario de edicion de versiones de contenido.

La clase ``RechazadoEditForm`` es el formulario de edicion de contenidos en estado rechazado.



.. automodule:: contenido.forms
   :members:
   :undoc-members:
   :show-inheritance:


contenido.models module
-----------------------

Modelos de Contenido
~~~~~~~~~~~~~~~~~~~~

La clase ``Cotenido`` es el modelo de contenido que importa RichTextField de CKEditorWidget para el texto enriquecido.
El modelo cuenta con 5 estados, y algunos permisos necesarios para el funcionamiento correcto del programa.

La clase ``Categoria`` es el modelo de categoria que posee un campo de moderacion.

La clase ``VersionContenido`` es el modelo para realizar un historial de cambios(versiones) del contenido.

La clase ``Like`` es el modelo para dar likes a los contenidos.

La clase ``Image`` es el modelo para insertar imagenes en el texto y guardarlas en la nube.

La clase ``Video`` es el modelo para insertar videos en el texto y guardarlas en la nube.

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
      
      path('publicar/<int:pk>/', views.apublicar_contenido, name='a-publicar'),
      path('publicar/',views.ContenidosApublicarView.as_view(),name= 'list_a_publicar'),
      path('revision/', views.ListarRevisionesView.as_view(), name='listar_revisiones'),
      path('contenido/<int:pk>/publicar/', views.publicar_contenido, name='publicar_contenido'),
      path('contenido/<int:pk>/rechazar/', views.rechazar_contenido, name='rechazar_contenido'),

      path('borradores/', views.ContenidoBorradorListView.as_view(), name='borradores_lista'),
      path('rechazados/', views.ContenidoRechazadoListView.as_view(), name='rechazados_lista'),

      path('contenido/<int:contenido_id>/toggle-like/', views.toggle_like, name='toggle_like'),
      path('contenido/<int:pk>/', views.detalle_contenido, name='detalle_contenido'),

      path('contenido/<int:pk>/editar/', views.EditarContenidoView.as_view(), name='editar-contenido'),
      path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
      path('delete_video/<int:video_id>/', views.delete_video, name='delete_video'),

      path('autor/<int:pk>/', views.detalle_autor, name='detalle_autor'),

      path('kanban/', views.kanban_view, name='kanban'),

      path('borrador/<int:pk>/editar/', views.EditarBorradorView.as_view(), name='editar-borrador'),
      path('version/<int:version_id>/editar/', views.editar_version, name='editar-version'),
      path('rechazado/<int:pk>/editar/', views.EditarRechazadoView.as_view(), name='editar-rechazado'),

      path('error/', views.error403, name='error403'),
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

La clase ``ContenidosApublicarView`` es la vista para mostrar contenidos a publicar.

La funcion ``apublicar_contenido`` es la encargada de mandar contenidos de en revision a publicar.

La funcion ``publicar_contenido`` es la encargada de mandar contenido a publicar a publicado.

La funcion ``rechazar_contenido`` es la encargada de rechazar un contenido a publicar.

La clase ``ContenidoBorradorListView`` es la vista de la lista de los borradores del contenido creado por el autor.

La clase ``ContenidoRechazadoListView`` es la vista de la lista contenidos rechazados.

La funcion ``detalle_contenido`` es la encargada de mostrar el detalle de los contenidos (likes ,comentarios).

La funcion ``toggle_like`` es la funcion encargada de dar o quitar el like en una publicacion.

La clase ``EditarContenidoView`` es la vista para editar el contenido en revision.

La clase ``EditarBorradorView`` es la vista para editar el contenido en borrador.

La clase ``EditarRechazadoView`` es la vista para editar el contenido rechazado.

La funcion ``detalle_autor`` es la funcion para ver los contenidos de un autor en especifico.

La funcion ``kanban_view`` es la funcion que muestra el kanban correspondiente al usuario logueado.

La funcion ``delete_image`` es la funcion para eliminar una imagen del contenido de texto enriquesido.

La funcion ``delete_video`` es la funcion para eliminar un video del contenido de texto enriquesido.

La clase ``ContenidoVersionListView`` es la vista de la lista de las versiones del contenido.

La clase ``editar_version`` es la funcion encargada de elejir la version deseada y usarla como ultima version (solo para borradores).





.. automodule:: contenido.views
   :members:
   :undoc-members:
   :show-inheritance:



.. automodule:: contenido
   :members:
   :undoc-members:
   :show-inheritance:
