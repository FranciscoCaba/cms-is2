from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
urlpatterns = [
    path('crear', login_required(views.ContenidoFormView.as_view()) , name='crear'),
    path('categoria/crear', login_required(views.CategoriaFormView.as_view()), name='categoria/crear'),
]
