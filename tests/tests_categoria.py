from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from contenido.models import Categoria
from contenido.forms import CategoriaForm

class CreateCategoria(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.permission_add = Permission.objects.get(codename='add_categoria')
        self.permission_change = Permission.objects.get(codename='change_categoria')
        self.permission_delete = Permission.objects.get(codename='delete_categoria')
        self.user.user_permissions.set([self.permission_add, self.permission_change, self.permission_delete])
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_categoria_creation(self):
        data = {
            'nombre': 'Categoria1',
            'moderada': False,
        }
        response = self.client.post(reverse('categoria-crear'), data)
        self.assertEqual(response.status_code, 302)  
        created_categoria = Categoria.objects.first()
        self.assertIsNotNone(created_categoria)
        self.assertEqual(created_categoria.nombre, 'Categoria1')
        self.assertFalse(created_categoria.moderada)
        self.assertTrue(created_categoria.is_active)

class CategoriaViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.permission_add = Permission.objects.get(codename='add_categoria')
        self.permission_change = Permission.objects.get(codename='change_categoria')
        self.permission_delete = Permission.objects.get(codename='delete_categoria')
        self.user.user_permissions.set([self.permission_add, self.permission_change, self.permission_delete])
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        self.categoria = Categoria.objects.create(
            nombre='Categoria',
            moderada=False,
            is_active=True
        )

    def test_categoria_update_view(self):
        data = {
            'nombre': 'Updated Category',
            'moderada': True,
        }
        response = self.client.post(reverse('categoria-update', args=[self.categoria.pk]), data)
        self.assertEqual(response.status_code, 302)  
        self.categoria.refresh_from_db()
        self.assertEqual(self.categoria.nombre, 'Updated Category')
        self.assertEqual(self.categoria.moderada, True)

    def test_desactivar_categoria_view(self):
        response = self.client.get(reverse('desactivar-categoria', args=[self.categoria.pk]))
        self.assertEqual(response.status_code, 302)  
        self.categoria.refresh_from_db()
        self.assertFalse(self.categoria.is_active)

    def test_activar_categoria_view(self):
        self.categoria.is_active = False
        self.categoria.save()
        response = self.client.get(reverse('activar-categoria', args=[self.categoria.pk]))
        self.assertEqual(response.status_code, 302)  
        self.categoria.refresh_from_db()
        self.assertTrue(self.categoria.is_active)
