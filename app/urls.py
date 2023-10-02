from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from.views import ProfileView, IndexView, UserListView, UserDetailView, UserCreateView, UserUpdateView, DesactivarUsuarioView, ActivarUsuarioView

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
