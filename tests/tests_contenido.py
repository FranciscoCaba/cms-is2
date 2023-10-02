from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from contenido.models import Contenido, Categoria, Image, Video
from contenido.forms import ContenidoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class ContenidoFormViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.permission_add = Permission.objects.get(codename='add_contenido')
        self.permission_change = Permission.objects.get(codename='change_contenido')
        self.permission_delete = Permission.objects.get(codename='delete_contenido')
        self.user.user_permissions.set([self.permission_add, self.permission_change, self.permission_delete])
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_contenido_creation(self):
        categoria = Categoria.objects.create(
            nombre='Categoria',
            moderada=True,
            is_active=True
        )
        data = {
            'titulo': 'Titulo',
            'categoria': categoria.id,
            'descripcion': 'Descripcion',
        }
        response = self.client.post(reverse('contenido-crear'), data)
        print(response.content.decode())  # Print the response content for debugging
        self.assertEqual(response.status_code, 302,'Error al cargar pagina')  
        created_contenido = Contenido.objects.first()
        self.assertIsNotNone(created_contenido,'Contenido no creado')
        self.assertEqual(created_contenido.titulo, 'Titulo','Titulo incorrecto')
        self.assertEqual(created_contenido.categoria, categoria,'Categoria no existe')
        self.assertEqual(created_contenido.descripcion, 'Descripcion','Descripcion incorrecta')

class VideoModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        categoria = Categoria.objects.create(
            nombre='Categoria',
            moderada=True,
            is_active=True
        )
        self.contenido = Contenido.objects.create(
            titulo='Sample Contenido',
            categoria_id=categoria.id, 
            descripcion='Sample Description',
            user=self.user
        )
    def test_video_creation(self):
        sample_video_path = os.path.join(os.path.dirname(__file__), 'video_test.mp4')
        sample_video = SimpleUploadedFile(
            name='video_test.mp4',
            content=open(sample_video_path, 'rb').read(),
            content_type='video/mp4' 
        )
        video = Video.objects.create(
            video=sample_video,
            contenido=self.contenido  
        )
        self.assertTrue(video.video.url.startswith('https://res.cloudinary.com/')) 
        self.assertIsNotNone(video)
        self.assertEqual(video.contenido, self.contenido)

class ImageModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        categoria = Categoria.objects.create(
            nombre='Categoria',
            moderada=True,
            is_active=True
        )
        self.contenido = Contenido.objects.create(
            titulo='Sample Contenido',
            categoria_id=categoria.id, 
            descripcion='Sample Description',
            user=self.user
        )
    def test_upload_image(self):
        sample_image_path = os.path.join(os.path.dirname(__file__), 'imagen_test.png')
        sample_image = SimpleUploadedFile(
            name='imagen_test.png',
            content=open(sample_image_path, 'rb').read(),
            content_type='image/png' 
        )
        image = Image.objects.create(
            image=sample_image,
            contenido=self.contenido  
        )
        self.assertTrue(image.image.url.startswith('https://res.cloudinary.com/')) 
        self.assertIsNotNone(image)
        self.assertEqual(image.contenido, self.contenido)