from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from.views import ProfileView, IndexView, UserListView, UserDetailView, UserCreateView, UserUpdateView, DesactivarUsuarioView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('profile/', login_required(ProfileView.as_view()), name='profile'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('delete/', views.delete, name='delete'),
    path('logout/', views.exit, name='exit'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('user/create/', UserCreateView.as_view(), name='user-create'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('desactivar_usuario/<int:pk>/', DesactivarUsuarioView.as_view(), name='desactivar-usuario'),
]
