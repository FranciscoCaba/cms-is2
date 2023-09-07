contenido package
=================

Submodules
----------


contenido.apps module
---------------------

.. automodule:: contenido.apps
   :members:
   :undoc-members:
   :show-inheritance:





contenido.forms module
----------------------

Formularios de Contenido
~~~~~~~~~~~~~~~~~~~~~~~~

La clase ``ContenidoForm`` importa una libreria llamada
``CKEditorWidget`` que nos permite utilizar texto enriquecido
La clase ``CategoriaForm`` posee un campo de moderacion

.. automodule:: contenido.forms
   :members:
   :undoc-members:
   :show-inheritance:






contenido.models module
-----------------------

Modelos de Contenido
~~~~~~~~~~~~~~~~~~~~~~~~

Creamos 2 clases ``Categoria`` y ``Contenido`` con sus respectivos campos
la clase ``Cotenido`` importa RichTextField de CKEditorWidget para el texto enriquecido


.. automodule:: contenido.models
   :members:
   :undoc-members:
   :show-inheritance:

contenido.urls module
---------------------


::

   urlpatterns = [
      path('crear', login_required(views.ContenidoFormView.as_view()) , name='crear'),
      path('categoria/crear', login_required(views.CategoriaFormView.as_view()), name='categoria/crear'),
   ]


contenido.views module
----------------------

.. automodule:: contenido.views
   :members:
   :undoc-members:
   :show-inheritance:



.. automodule:: contenido
   :members:
   :undoc-members:
   :show-inheritance:
