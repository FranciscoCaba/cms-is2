from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
urlpatterns = [
    path('create', login_required(views.ContenidoFormView.as_view()) , name='create'),
]
