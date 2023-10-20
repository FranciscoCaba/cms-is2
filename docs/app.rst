app package
===========

Aqui se encuentran toda la gestion de roles y usuarios que maneja el sistema

app.urls module
---------------

Urls del proyecto
~~~~~~~~~~~~~~~~~~

Estos son los path(caminos) del proyecto

::
   
   urlpatterns = [
      path('', IndexView.as_view(), name='index'),
      path('profile/', login_required(ProfileView.as_view()), name='profile'),
      path('register/', views.register, name='register'),
      path('edit/', login_required(views.edit), name='edit'),
      path('delete/', login_required(views.delete), name='delete'),
      path('logout/', views.exit, name='exit'),
      path('users/', login_required(UserListView.as_view()), name='user-list'),
      path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
      path('user/create/', UserCreateView.as_view(), name='user-create'),
      path('user/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
      path('desactivar_usuario/<int:pk>/', DesactivarUsuarioView.as_view(), name='desactivar-usuario'),
      path('activar_usuario/<int:pk>/', ActivarUsuarioView.as_view(), name='activar-usuario'),
      path('roles/create', login_required(views.create_group), name='create_group'),
      path('roles/delete/<int:group_id>/', login_required(views.delete_group), name='delete_group'),
      path('roles/edit/<int:group_id>/', login_required(views.edit_group), name='edit_group'),
      path('roles/', login_required(views.group_list), name='group_list'),
   ]


app.forms module
----------------

Formularios del Proyecto
~~~~~~~~~~~~~~~~~~~~~~~~

La clase ``CustomUserCreationForm`` es un formulario para la creacion de usuario.

::

   Posee los campos de = ['nombre de usuario', 'nombre ', 'apellido ', 'email', 'roll']


La clase ``CustomUserChangeForm`` es un formulario para la edicion de usuario.

::

   Posee = ['nombre de usuario', 'nombre', 'apellido', 'email', 'contrasena1', 'contrasena1']


La clase ``CustomAdminUserCreationForm`` es un formulario para la creacion de usuario desde el panel de administracion.
   
::

   Posee los campos de = ['nombre de usuario', 'nombre', 'apellido']


La clase ``CustomAdminUserChangeForm`` es un formulario para la edicion de usuario desde el panel de administracion.

::

   Posee los campos de = ['nombre de usuario', 'nombre', 'apellido']


La clase ``GroupCreationForm`` es un formulario para la creacion de roles.

::

   Posee los campos de  = ['nombre', 'permisos']


La clase ``GroupEditForm`` es un formulario para la edicion de roles.

::

   Posee los campos de  = ['nombre', 'permisos']


.. automodule:: app.forms
   :members:
   :undoc-members:
   :show-inheritance:

  
app.views module
----------------

Vistas del Proyecto
~~~~~~~~~~~~~~~~~~~

La clase ``PaginaNoEncontradaView`` es la vista que se genera al entrar a una url que no existe (error 404).

::

   hace un ``get(request, *args, **kwargs)``.
   Necesita los permisos de = 'auth.delete_user'.
   usa el template = 'activar_usuario.html'.


La clase ``CustomTemplateView(TemplateView):`` es una vista base cuyo proposito es darle contexto a las vistas del usuario logeado.
   
La clase ``ProfileView(CustomTemplateView):`` muestra el perfil existente del usuario.

La clase ``IndexView(CustomTemplateView):`` muestra la pagina principal

El metodo ``register`` es la vista dedicada al registro de usuario, para los visitantes de la pagina.

El metodo ``edit`` es la vista dedicada a la modificacion de la informacion del usuario con sesion activa.

El metodo ``delete`` es un metodo dedicado para dar de baja a la cuenta del usuario con sesion activa.

El metodo ``exit`` es un metodo dedicado para cerrar sesion del usuario con sesion activa.

El metodo ``create_group`` es la vista dedicada a la creacion de roles.

El metodo ``delete_group`` es un metodo dedicado a dar de baja a un rol.

El metodo ``edit_group`` es una vista para actualizar los roles.

El metodo ``group_list`` es una vista para listar los roles.

La clase ``UserListView`` es la vista dedicada a listar todos los usuarios desde el panel de administracion.

::

   utiliza el objeto = 'user'.
   utiliza el template = 'user_list.html'.


La clase ``UserDetailView`` es la vista dedicada a la gestion de detalles de usuarios desde el panel de administracion.

::

   utiliza el objeto = 'user'.
   utiliza el template = 'user_detail.html'.


La clase ``UserCreateView`` es la vista dedicada a la creacion de usuario desde el panel de administracion.
   
::

   utiliza el form = CustomAdminUserCreationForm.
   Requiere el permiso  = 'auth.add_user'.
   la url exitosa es = '/users/'.
   el template que utiliza es = 'user_form.html'.


La clase ``UserUpdateView`` es la vista dedicada para actualizar a los usuarios desde el panel de administracion.

::

   utiliza el form = CustomAdminUserChangeForm.
   requiere del permiso = 'auth.change_user'.
   la url exitosa es = '/users/'.
   utiliza el template = 'user_form.html'.


La clase ``DesactivarUsuarioView`` es la vista dedicada para dar de baja a un usuario desde el panel de administracion.

::
   
   usa una funcion = ``get(request, *args, **kwargs)``.
   Requiere del permiso = 'auth.delete_user'.
   utiliza el template = 'desactivar_usuario.html.


La clase ``ActivarUsuarioView`` es la vista dedicada para reactivar a un usuario desde el panel de administracion.



.. automodule:: app.views
   :members: 
   :undoc-members:
   :show-inheritance:



.. automodule:: app
   :members:
   :undoc-members:
   :show-inheritance:
