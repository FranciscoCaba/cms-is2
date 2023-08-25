from django.urls import path
from . import views
from.views import ProfileView, IndexView
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', views.exit, name='exit'),
]
