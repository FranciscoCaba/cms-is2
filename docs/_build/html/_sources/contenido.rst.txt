contenido package
=================

contenido.forms module
----------------------

Formularios de Contenido
~~~~~~~~~~~~~~~~~~~~~~~~

La clase ``ContenidoForm`` importa una libreria llamada ``CKEditorWidget`` que nos permite utilizar texto enriquecido.

::


   campos de = ('titulo', 'resumen', 'categoria', 'descripcion', 'solo_suscriptores')

   modelo Contenido

   widgets = 'categoria' objeto tipo Select, 
   'descripcion' objeto tipo CharField, 
   'resumen' objeto tipo TextInput, 
   'solo_suscriptores' objeto tipo CheckboxInput, 
   'titulo' objeto tipo TextInput 
   

La clase ``ContenidoEditForm`` es el formulario de la vista de edicion de contenido.

::


   Posee los campos de = ('titulo', 'resumen', 'categoria', 'descripcion', 'solo_suscriptores')

   modelo Contenido

   widgets = 'categoria' objeto tipo Select, 
   'descripcion' objeto tipo CharField, 
   'resumen' objeto tipo TextInput, 
   'solo_suscriptores' objeto tipo CheckboxInput, 
   'titulo' objeto tipo TextInput


La clase ``CategoriaForm`` forumalio para la creacion de categoria.

::

   Los campos que posee son = ['nombre', 'moderada']

   modelo Categoria

   utiliza widgets = 'moderada' objeto tipo CheckboxInput,
   'nombre' objeto tipo TextInput 


La clase ``CategoriaEditForm``  formulario para la edicion de categoria.

::


   Los campos que posee son = ['nombre', 'moderada']

   modelo Categoria

   utiliza widgets = 'moderada': objeto tipo CheckboxInput, 
   'nombre'objeto tipo TextInput



La clase ``BorradorEditForm`` es el formulario de edicion de borrador de contenido.

::

   Los campos que posee son  = ('titulo', 'resumen', 'categoria', 'descripcion', 'solo_suscriptores')

   modelo Contenido

   utiliza widgets = 'categoria' tipo objeto Select , 
   'descripcion' tipo objeto CharField, 
   'resumen' tipo objeto TextInput , 
   'solo_suscriptores'tipo objeto CheckboxInput , 
   'titulo': tipo objeto TextInput 



La clase ``VersionContenidoEditForm`` es el formulario de edicion de versiones de contenido.

::


   campos  = ('titulo', 'resumen', 'categoria', 'descripcion', 'solo_suscriptores')

   modelo VersionContenido

   widgets = 'categoria' objeto tipo Select, 
   'descripcion' objeto tipo CharField, 
   'resumen' objeto tipo TextInput, 
   'solo_suscriptores' objeto tipo CheckboxInput, 
   'titulo' objeto tipo TextInput


La clase ``RechazadoEditForm`` es el formulario de edicion de contenidos en estado rechazado.

::


   campos = ('titulo', 'resumen', 'categoria', 'descripcion', 'solo_suscriptores')

   modelo  Contenido

   widgets = 'categoria' objeto tipo Select, 
   'descripcion' objeto tipo CharField, 
   'resumen' objeto tipo TextInput, 
   'solo_suscriptores' objeto tipo CheckboxInput, 
   'titulo' objeto tipo TextInput



.. automodule:: contenido.forms
   :members:
   :undoc-members:
   :show-inheritance:


contenido.models module
-----------------------

Modelos de Contenido
~~~~~~~~~~~~~~~~~~~~

La clase ``Cotenido`` es el modelo de contenido que importa RichTextField de CKEditorWidget para el texto enriquecido.

::
    
   El modelo cuenta con 5 estados, y algunos permisos necesarios para el funcionamiento correcto del programa.
   
   Los campos que posee son:

   ESTADO_CHOICES = (('borrador', 'Borrador'), ('revision', 'En revisión'), ('apublicar', 'A publicar'), ('rechazado', 'Rechazado'), ('publicado', 'Publicado'), ('inactivo', 'Inactivo'))

   categoria: Acceso al objeto relacionado en el lado adelante de una relación de muchos a uno o uno a uno (a través de una subclase ForwardOneToOneDescriptor).

   descripcion: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   estado: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   fecha: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   id: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   images: Acceso al gestor de objetos relacionados en el lado inverso de una relación de muchos a uno.

   is_active: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   like_set: Acceso al gestor de objetos relacionados en el lado inverso de una relación de muchos a uno.

   likes: Acceso al gestor de objetos relacionados en los lados directo e inverso de una relación de muchos a muchos.

   nota: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   reportado: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   resumen: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   save: Guardar la instancia actual. Sobrescribe esto en una subclase si deseas controlar el proceso de guardado.
   Los parámetros 'force_insert' y 'force_update' se pueden utilizar para insistir en que el "guardado" debe ser una inserción o 
   actualización de SQL (o equivalente para sistemas que no utilizan SQL), respectivamente. Normalmente, no deben establecerse.

   solo_suscriptores: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   titulo: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   user: Acceso al objeto relacionado en el lado directo de una relación de muchos a uno o de uno a uno (a través de una subclase ForwardOneToOneDescriptor).

   versiones: Acceso al gestor de objetos relacionados en el lado inverso de una relación de muchos a uno.

   videos: Acceso al gestor de objetos relacionados en el lado inverso de una relación de muchos a uno.



La clase ``Categoria`` es el modelo de categoria que posee un campo de moderacion.

::
   
  
   Los campos que posee son:

   Categoria: Acceso al gestor de objetos relacionados en el lado inverso de una relación de muchos a uno.

   id: Un envoltorio para un campo de carga diferida. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   categoria_version: Acceso al gestor de objetos relacionados en el lado opuesto de una relación de muchos a uno

   is_active: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   moderada: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   nombre: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.


La clase ``VersionContenido`` es el modelo para realizar un historial de cambios(versiones) del contenido.
::

   los campos que posee son:

   categoria: "Acceso al objeto relacionado en el lado directo de una relación de muchos a uno o de uno a uno (a través de una subclase de ForwardOneToOneDescriptor).

   contenido: "Acceso al objeto relacionado en el lado directo de una relación de muchos a uno o de uno a uno (a través de una subclase de ForwardOneToOneDescriptor).

   descripcion: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   estado: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   fecha_modificacion: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   id: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   nota: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   resumen: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   save: Guardar la instancia actual. Sobrescribe esto en una subclase si deseas controlar el proceso de guardado.
   Los parámetros 'force_insert' y 'force_update' se pueden utilizar para insistir en que el "guardado" debe ser una inserción o 
   actualización de SQL (o equivalente para sistemas que no utilizan SQL), respectivamente. Normalmente, no deben establecerse.

   solo_suscriptores: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   titulo: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   user_modificacion: Acceso al objeto relacionado en el lado directo de una relación de muchos a uno o de uno a uno (a través de una subclase de ForwardOneToOneDescriptor).

   version: Un envoltorio para un campo de carga aplazada. Cuando se lee el valor de este objeto por primera vez, se ejecuta la consulta.

   
La clase ``Like`` es el modelo para dar likes a los contenidos.

::

   Los campos que posee son:

   contenido: Accessor to the related object on the forward side of a many-to-one or one-to-one (via ForwardOneToOneDescriptor subclass) relation.
   
   created_ad: Un envoltorio para un campo de carga aplazada. Cuando el valor se lee de este objeto por primera vez, se ejecuta la consulta.

   id: Un envoltorio para un campo de carga aplazada. Cuando el valor se lee de este objeto por primera vez, se ejecuta la consulta.

   user: Acceso al objeto relacionado en el lado directo de una relación de muchos a uno o de uno a uno (a través de una subclase ForwardOneToOneDescriptor).


La clase ``Image`` es el modelo para insertar imagenes en el texto y guardarlas en la nube.

::

   Los campos que posee son:

   contenido: Accessor to the related object on the forward side of a many-to-one or one-to-one (via ForwardOneToOneDescriptor subclass) relation.
   
   id: Un envoltorio para un campo de carga aplazada. Cuando el valor se lee de este objeto por primera vez, se ejecuta la consulta.

   image: Similar al FileDescriptor, pero para ImageFields. La única diferencia es asignar el ancho/alto al campo width_field/height_field, si es apropiado.



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
      path('contenido/<int:pk>/', views.detalle_contenido, name='detalle_contenido'),

      path('contenido/<int:pk>/editar/', views.EditarContenidoView.as_view(), name='editar-contenido'),
      path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
      path('delete_video/<int:video_id>/', views.delete_video, name='delete_video'),

      path('autor/<int:pk>/', views.detalle_autor, name='detalle_autor'),

      path('kanban/', views.kanban_view, name='kanban'),
      path('kanban/all/', views.all_kanban_view, name='all_kanban'),

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

::


   utiliza el form ContenidoForm

   form_valid(form)

      Si el form es valido, relaciona con el modelo.

   get_form_kwargs()[source]

      Devuelve los argumentos de palabra clave para instanciar el formulario

   get_success_url()[source]

      Devuelve la URL a la que redirigir después de procesar un formulario válido.

   requiere del permiso = 'contenido.add_contenido'

   el url exitoso es = '/'

   el template que utiliza es  = 'contenido/contenido_crear.html'


La clase ``CategoriaFormView`` es la vista de la categoria con o sin moderacion.

::


   utiliza el form CategoriaForm

   valida el form, si el form es valido, guarda el modelo asociado.

   requiere del permiso = 'contenido.add_categoria'

   la url de exito es  = '/contenido/categoria'

   utiliza el template = 'categoria/categoria_crear.html'


La clase ``CategoriaListView`` es la vista de las categorias ya creadas.

::


   trae el objeto contexto = 'categorias'

   modelo Categoria

   utiliza el template = 'categoria/categoria_list.html'


La clase ``CategoriaDetailView`` es la vista de los detalles de la categoria.

::


   trae el objeto contexto = 'categoria'

   modelo Categoria

   utiliza el template  = 'categoria/categoria_detail.html'


La clase ``CategoriaUpdateView`` es la vista para la actualizacion de las categorias.

::


   utiliza el form CategoriaEditForm

   modelo Categoria

   requiere permiso de = 'contenido.change_categoria'

   la url de exito es  = '/contenido/categoria'

   el template que utiliza es  = 'categoria/categoria_edit.html'


La clase ``DesactivarCategoriaView`` sirve para dar de baja una categoria.

::


   get(request, *args, **kwargs)

   modelo Categoria

   requiere el permiso  = 'contenido.delete_categoria'

   utiliza el template = 'categoria/desactivar_categoria.html'



La clase ``ActivarCategoriaView`` sirve para reactivar una categoria.

::


   realiza un  get(request, *args, **kwargs)

   modelo Categoria

   necesita del permiso  = 'contenido.delete_categoria'

   utiliza el template  = 'categoria/activar_categoria.html'


La clase ``MostrarContenidosView`` es la vista para mostrar los contenidos. 

La clase ``ListarRevisionesView`` es la vista para mostrar los contenidos en revision.

::


   trae el objeto contexto = 'por_revisar'

   get_queryset()

     Devolver la lista de elementos para esta vista.

      El valor devuelto debe ser un iterable y puede ser una instancia de QuerySet, en cuyo caso se habilitará el comportamiento específico de QuerySet.
   
   modelo Contenido

   requiere el permiso = 'contenido.ver_revisiones'

   el nombre del template es = 'listar_revisiones.html'


La clase ``ContenidosApublicarView`` es la vista para mostrar contenidos a publicar.

::


   trae el objeto contexto = 'revisados'

   get_queryset()

      Devuelve la lista de elementos para esta vista.

   El valor devuelto debe ser un iterable y puede ser una instancia de QuerySet, en cuyo caso se habilitará el comportamiento específico de QuerySet.
   
   modelo Contenido

   utiliza el template = 'contenido/contenido_a_publicar.html'


La funcion ``apublicar_contenido`` es la encargada de mandar contenidos de en revision a publicar.

La funcion ``publicar_contenido`` es la encargada de mandar contenido a publicar a publicado.

La funcion ``rechazar_contenido`` es la encargada de rechazar un contenido a publicar.

La clase ``ContenidoBorradorListView`` es la vista de la lista de los borradores del contenido creado por el autor.

::


   trae el objeto contexto = 'contenidos_borrador'

   hace una funcion get_queryset()

      Devuelve la lista de elementos para esta vista.

      El valor de retorno debe ser iterable y puede ser una instancia de QuerySet, en cuyo caso se habilitará el comportamiento específico de QuerySet.

   modelo Contenido

   requiere del permiso = 'contenido.add_contenido'

   utiliza el template = 'borrador/borradores_lista.html'


La clase ``ContenidoRechazadoListView`` es la vista de la lista contenidos rechazados.

::


   trae el objeto contexto = 'contenidos_rechazados'

   get_queryset()

      Devuelve la lista de elementos para esta vista.

      El valor de retorno debe ser un iterable y puede ser una instancia de QuerySet, en cuyo caso se habilitará el comportamiento específico de QuerySet.

   modelo Contenido

   requiere del permiso = 'contenido.add_contenido'

   utiliza el template = 'contenido/rechazados_lista.htm


La funcion ``detalle_contenido`` es la encargada de mostrar el detalle de los contenidos (likes ,comentarios).

La funcion ``toggle_like`` es la funcion encargada de dar o quitar el like en una publicacion.

La clase ``EditarContenidoView`` es la vista para editar el contenido en revision.

::


   utiliza el form ContenidoEditForm

   form_valid(form)

      Si el form es correcto, guarda el modelo asociado.

   modelo Contenido

   requiere del permiso = 'contenido.change_contenido'

   url exitosa = '/contenido/revision/'

   nombre del template  = 'contenido/contenido_editar.html'


La clase ``EditarBorradorView`` es la vista para editar el contenido en borrador.

::

   utiliza el formulario BorradorEditForm

   form_valid(form)

      Si el form es valido, guarda el modelo asociado.

   get_form_kwargs()

      Devuelve los argumentos de palabra clave para instanciar el formulario.

   modelo Contenido

   url exitosa = '/contenido/borradores/'

   el template que utiliza es  = 'borrador/borrador_editar.html'


La clase ``EditarRechazadoView`` es la vista para editar el contenido rechazado.

::


   utiliza el form RechazadoEditForm

   form_valid(form)

      Si el form es valido, guarda el modelo asociado.

   get_form_kwargs()

      Devuelve los argumentos de palabra clave para instanciar el formulario.

   modelo Contenido

   url exitosa = '/contenido/rechazados/'

   utiliza el template = 'contenido/rechazado_editar.html'


La funcion ``detalle_autor`` es la funcion para ver los contenidos de un autor en especifico.

La funcion ``kanban_view`` es la funcion que muestra el kanban correspondiente al usuario logueado.

La funcion ``delete_image`` es la funcion para eliminar una imagen del contenido de texto enriquesido.

La funcion ``delete_video`` es la funcion para eliminar un video del contenido de texto enriquesido.

La clase ``ContenidoVersionListView`` es la vista de la lista de las versiones del contenido.

La clase ``editar_version`` es la funcion encargada de elejir la version deseada y usarla como ultima version (solo para borradores).

La clase ``UnContenidoApublicarView`` es la vista para un contenido a publicar 

::


   trae el objeto contexto = 'revisados'

   get_queryset()

      Devolver la lista de elementos para esta vista.

      El valor de retorno debe ser un iterable y puede ser una instancia de QuerySet, en cuyo caso se habilitará el comportamiento específico de QuerySet.
   
   modelo Contenido

   utiliza el template = 'contenido/contenido_a_publicar.html'



.. automodule:: contenido.views
   :members:
   :undoc-members:
   :show-inheritance:



.. automodule:: contenido
   :members:
   :undoc-members:
   :show-inheritance:
