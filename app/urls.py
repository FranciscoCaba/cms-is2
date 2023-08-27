from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from.views import ProfileView, IndexView
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('profile/', login_required(ProfileView.as_view()), name='profile'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('logout/', views.exit, name='exit'),
]
