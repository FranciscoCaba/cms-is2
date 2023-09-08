from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from contenido.models import Contenido, Categoria
from contenido.forms import ContenidoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin

class ContenidoFormViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.permission_add = Permission.objects.get(codename='add_contenido')
        self.user.user_permissions.add(self.permission_add)
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_contenido_creation(self):
        categoria = Categoria.objects.create(
            nombre='Categoria',
            moderada=False,
            is_active=True
        )
        data = {
            'titulo': 'Titulo',
            'categoria': categoria.id,
            'descripcion': 'Descripcion',
        }
        response = self.client.post(reverse('contenido-crear'), data)
        self.assertEqual(response.status_code, 302)  
        created_contenido = Contenido.objects.first()
        self.assertIsNotNone(created_contenido)
        self.assertEqual(created_contenido.titulo, 'Titulo')
        self.assertEqual(created_contenido.categoria, categoria)
        self.assertEqual(created_contenido.descripcion, 'Descripcion')
