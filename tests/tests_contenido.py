from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from contenido.models import Contenido, Categoria, Image, Video, Archivos, VersionContenido, Like, Favoritos, Dislike, Calificacion
from contenido.forms import ContenidoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail
from django.core.mail import send_mail
from django.test import override_settings
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
        categoria = Categoria.objects.create(nombre='Categoria',moderada=True,is_active=True)
        data = {
            'titulo': 'Titulo',
            'categoria': categoria.id,
            'descripcion': 'Descripcion',
            'resumen': 'Resumen',
        }
        response = self.client.post(reverse('contenido-crear'), data)
        self.assertEqual(response.status_code, 302,'Error al cargar pagina')  
        created_contenido = Contenido.objects.first()
        self.assertIsNotNone(created_contenido,'Contenido no creado')
        self.assertEqual(created_contenido.titulo, 'Titulo','Titulo incorrecto')
        self.assertEqual(created_contenido.categoria, categoria,'Categoria no existe')
        self.assertEqual(created_contenido.descripcion, 'Descripcion','Descripcion incorrecta')

    def test_contenido_creation_creates_revision(self):
        categoria = Categoria.objects.create(nombre='Categoria',moderada=True,is_active=True)
        data = {
            'titulo': 'Titulo',
            'categoria': categoria.id,
            'descripcion': 'Descripcion',
            'crear': 'Crear',  
            'resumen': 'Resumen',
        }
        response = self.client.post(reverse('contenido-crear'), data)
        self.assertEqual(response.status_code, 302, 'Error al cargar pagina')  
        created_contenido = Contenido.objects.first()
        self.assertIsNotNone(created_contenido, 'Contenido no creado')
        self.assertEqual(created_contenido.estado, 'En revisión', 'Estado del contenido incorrecto')

    def test_contenido_creation_creates_borrador(self):
        categoria = Categoria.objects.create(nombre='Categoria',moderada=True,is_active=True)
        data = {
            'titulo': 'Titulo',
            'categoria': categoria.id,
            'descripcion': 'Descripcion',
            'borradorcito': 'Guardar Borrador', 
            'resumen': 'Resumen',
        }
        response = self.client.post(reverse('contenido-crear'), data)
        self.assertEqual(response.status_code, 302, 'Error al cargar pagina')  
        created_contenido = Contenido.objects.first()
        self.assertIsNotNone(created_contenido, 'Contenido no creado')
        self.assertEqual(created_contenido.estado, 'Borrador', 'Estado del contenido incorrecto')

    def test_edit_contenido_in_revision(self):
        categoria = Categoria.objects.create(nombre='Categoria',moderada=True,is_active=True)
        contenido = Contenido.objects.create(
            categoria=categoria,
            user=self.user,
            titulo='Original Title',
            descripcion='Original Description',
            estado='En revisión',
        )
        data = {
            'titulo': 'Edited Title',
            'categoria': categoria.id,
            'descripcion': 'Edited Description',
            'resumen': 'Resumen',
        }
        response = self.client.post(reverse('editar-contenido', kwargs={'pk': contenido.pk}), data)
        self.assertEqual(response.status_code, 302, 'Error al cargar pagina')  
        edited_contenido = Contenido.objects.get(pk=contenido.pk)
        self.assertEqual(edited_contenido.titulo, 'Edited Title', 'Titulo incorrecto')
        self.assertEqual(edited_contenido.descripcion, 'Edited Description', 'Descripcion incorrecta')

    def test_edit_borrador(self):
        categoria = Categoria.objects.create(nombre='Categoria', moderada=True, is_active=True)
        contenido = Contenido.objects.create(
            categoria=categoria,
            user=self.user,
            titulo='Original Title',
            descripcion='Original Description',
            estado='Borrador',
            resumen='Original Resumen'
        )
        data = {
            'titulo': 'Edited Title',
            'categoria': categoria.id,
            'descripcion': 'Edited Description',
            'resumen': 'Edited Resumen',
        }
        response = self.client.post(reverse('editar-borrador', kwargs={'pk': contenido.pk}), data)
        self.assertEqual(response.status_code, 302, 'Error al cargar página')
        edited_contenido = Contenido.objects.get(pk=contenido.pk)
        self.assertEqual(edited_contenido.titulo, 'Edited Title', 'Titulo incorrecto')
        self.assertEqual(edited_contenido.resumen, 'Edited Resumen', 'Resumen incorrecto')
        self.assertEqual(edited_contenido.descripcion, 'Edited Description', 'Descripción incorrecta')
        self.assertFalse(edited_contenido.solo_suscriptores, 'Solo Suscriptores incorrecto')

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
        self.assertTrue(video.video.url.startswith('https://res.cloudinary.com/'), 'Video no creado') 
        self.assertIsNotNone(video, 'Video no creado')
        self.assertEqual(video.contenido, self.contenido, 'Contenido incorrecto')

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
        self.assertTrue(image.image.url.startswith('https://res.cloudinary.com/'), 'Imagen no creada') 
        self.assertIsNotNone(image, 'Imagen no creada')
        self.assertEqual(image.contenido, self.contenido, 'Contenido incorrecto')

class ArchivosModelTest(TestCase):
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

    def test_archivos_creation(self):
        sample_archivo_path = os.path.join(os.path.dirname(__file__), 'sample.pdf')
        sample_archivo = SimpleUploadedFile(
            name='sample.pdf',
            content=open(sample_archivo_path, 'rb').read(),
            content_type='application/pdf'
        )
        archivo = Archivos.objects.create(
            contenido=self.contenido,
            archivo=sample_archivo
        )
        self.assertTrue(archivo.archivo.url.startswith('https://res.cloudinary.com/'), 'Archivo no creado')
        self.assertIsNotNone(archivo, 'Archivo no creado')
        self.assertEqual(archivo.contenido, self.contenido, 'Contenido incorrecto')

class EstadoChangeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.user_permissions.add(Permission.objects.get(codename='puede_publicar_rechazar'))
        self.user.user_permissions.add(Permission.objects.get(codename='puede_editar_aceptar'))
        categoria = Categoria.objects.create(nombre='Categoria',moderada=True,is_active=True)
        self.contenido = Contenido.objects.create(titulo='Test Contenido',categoria_id=categoria.id ,user=self.user, estado='En revisión')

    def test_apublicar_contenido(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('a-publicar', args=[self.contenido.pk])
        note = "Test"
        response = self.client.post(url, {'nota': note})
        self.contenido.refresh_from_db()  
        self.assertEqual(self.contenido.estado, 'A publicar')

    def test_publicar_contenido(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('publicar_contenido', args=[self.contenido.pk])
        note = "Test"
        response = self.client.post(url, {'nota': note})
        self.contenido.refresh_from_db()  
        self.assertEqual(self.contenido.estado, 'Publicado')

    def test_rechazar_contenido(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('rechazar_contenido', args=[self.contenido.pk])
        note = "Test"
        response = self.client.post(url, {'nota': note})
        self.contenido.refresh_from_db() 
        self.assertEqual(self.contenido.estado, 'Rechazado')

class EmailTest(TestCase):
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_email(self):
        subject = 'Test Email'
        message = 'This is a test email.'
        from_email = 'from@example.com'
        recipient_list = ['to@example.com']
        send_mail(subject, message, from_email, recipient_list)
        self.assertEqual(len(mail.outbox), 1)
        sent_email = mail.outbox[0]
        self.assertEqual(sent_email.subject, subject)
        self.assertEqual(sent_email.body, message)
        self.assertEqual(sent_email.from_email, from_email)
        self.assertEqual(sent_email.to, recipient_list)

class EditVersionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.is_staff = True  
        self.user.save()
        self.client.login(username='testuser', password='testpassword')

    def create_version(self):
        categoria = Categoria.objects.create(nombre='Categoria',moderada=True,is_active=True)
        contenido = Contenido.objects.create(
            categoria=categoria,
            user=self.user,
            titulo='Original Title',
            descripcion='Original Description',
            estado='Borrador',
            resumen='Original Resumen'
        )
        version = VersionContenido.objects.create(
            contenido=contenido,
            user_modificacion=self.user,
            categoria=categoria,
            titulo='Original Title',
            descripcion='Original Description',
            estado='Borrador',
        )
        return version

    def test_edit_version_view(self):
        version = self.create_version()
        data = {
            'titulo': 'Edited Title',
            'resumen': 'Edited Resumen',
            'categoria': version.categoria.id,
            'descripcion': 'Edited Description',
        }
        response = self.client.post(reverse('editar-version', kwargs={'version_id': version.id}), data)
        self.assertEqual(response.status_code, 302, 'Error al cargar página')
        edited_version = VersionContenido.objects.get(id=version.id+1)
        self.assertEqual(edited_version.titulo, 'Edited Title', 'Titulo incorrecto')
        self.assertEqual(edited_version.resumen, 'Edited Resumen', 'Resumen incorrecto')
        self.assertEqual(edited_version.descripcion, 'Edited Description', 'Descripción incorrecta')

class Reacciones(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.categoria = Categoria.objects.create(nombre='Test Categoria')
        self.contenido = Contenido.objects.create(titulo='Test Content', user=self.user, categoria=self.categoria)
        self.like_url = reverse('toggle_like', args=[self.contenido.id])
        self.dislike_url = reverse('toggle_dislike', args=[self.contenido.id])
        self.favorito_url = reverse('toggle_favorito', args=[self.categoria.id])

    def test_like(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.like_url)
        self.assertTrue(Like.objects.filter(user=self.user, contenido=self.contenido).exists())
        self.assertEqual(self.contenido.likes.count(), 1)

    def test_unlike(self):
        self.client.login(username='testuser', password='testpassword')
        Like.objects.create(user=self.user, contenido=self.contenido)
        response = self.client.get(self.like_url)
        self.assertFalse(Like.objects.filter(user=self.user, contenido=self.contenido).exists())
        self.assertEqual(self.contenido.likes.count(), 0)
    
    def test_dislike(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.dislike_url)
        self.assertTrue(Dislike.objects.filter(user=self.user, contenido=self.contenido).exists())
        self.assertEqual(self.contenido.dislikes.count(), 1)

    def test_undislike(self):
        self.client.login(username='testuser', password='testpassword')
        Dislike.objects.create(user=self.user, contenido=self.contenido)
        response = self.client.get(self.dislike_url)
        self.assertFalse(Dislike.objects.filter(user=self.user, contenido=self.contenido).exists())
        self.assertEqual(self.contenido.dislikes.count(), 0)

    def test_favorito(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.favorito_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Favoritos.objects.filter(user=self.user, categoria=self.categoria).exists())
        self.assertEqual(self.categoria.seguidores.count(), 1)

    def test_unfavorito(self):
        self.client.login(username='testuser', password='testpassword')
        Favoritos.objects.create(user=self.user, categoria=self.categoria)
        response = self.client.get(self.favorito_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Favoritos.objects.filter(user=self.user, categoria=self.categoria).exists())
        self.assertEqual(self.categoria.seguidores.count(), 0)

    def test_compartir_contenido(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('compartir_contenido', args=[self.contenido.id])
        response = self.client.post(url)
        self.contenido.refresh_from_db() 
        self.assertEqual(self.contenido.compartidos, 1)

class CalificacionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.categoria = Categoria.objects.create(nombre='Test Categoria')
        self.contenido = Contenido.objects.create(titulo='Test Content', user=self.user, categoria=self.categoria)

    def test_create_calificacion(self):
        response = self.client.post(reverse('detalle_contenido', kwargs={'pk': self.contenido.id}), {'estrellas': '5'})
        self.assertEqual(response.status_code, 302)  
        calificacion = Calificacion.objects.filter(contenido=self.contenido, usuario=self.user).first()
        self.assertIsNotNone(calificacion)  

    def test_update_calificacion(self):
        calificacion = Calificacion.objects.create(contenido=self.contenido, usuario=self.user, estrellas=4)
        response = self.client.post(reverse('detalle_contenido', kwargs={'pk': self.contenido.id}), {'estrellas': '3'})
        self.assertEqual(response.status_code, 302)  
        calificacion.refresh_from_db()
        self.assertEqual(calificacion.estrellas, 3)  

    def test_delete_calificacion(self):
        calificacion = Calificacion.objects.create(contenido=self.contenido, usuario=self.user, estrellas=4)
        response = self.client.post(reverse('detalle_contenido', kwargs={'pk': self.contenido.id}), {'estrellas': '0'})
        self.assertEqual(response.status_code, 302)  
        calificacion_exists = Calificacion.objects.filter(contenido=self.contenido, usuario=self.user).exists()
        self.assertFalse(calificacion_exists)  