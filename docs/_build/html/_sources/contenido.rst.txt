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
      path('categoria/crear', login_required(views.CategoriaFormView.as_view()), name='categoria-crear'),
      path('categoria', views.CategoriaListView.as_view(), name='categoria-list'),
      path('categoria/<int:pk>/', views.CategoriaDetailView.as_view(), name='categoria-detail'),
      path('categoria/<int:pk>/update/', views.CategoriaUpdateView.as_view(), name='categoria-update'),
      path('categoria/<int:pk>/desactivar', views.DesactivarCategoriaView.as_view(), name='desactivar-categoria'),
      path('categoria/<int:pk>/activar', views.ActivarCategoriaView.as_view(), name='activar-categoria'),
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


.. automodule:: contenido.views
   :members:
   :undoc-members:
   :show-inheritance:



.. automodule:: contenido
   :members:
   :undoc-members:
   :show-inheritance:
