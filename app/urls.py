from django.urls import path
from . import views
from.views import ProfileView
urlpatterns = [
    path('', views.index, name='index'),

    path('profile/', ProfileView.as_view(), name='profile'),
]
