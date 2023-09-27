from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.core.files.storage import default_storage 
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from cloudinary_storage.validators import validate_video
# Create your models here.
class Categoria(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=True)
    nombre = models.CharField(max_length=100)
    moderada = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
class Contenido(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='categoria', verbose_name='Categoria',default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuario', verbose_name='Usuario')
    titulo = models.CharField(max_length=100)
    #estado = models.CharField(default='Borrador', max_length=100)
    descripcion = RichTextField()
    likes = models.ManyToManyField(User, through='Like', related_name='contenido_likes')
    is_active = models.BooleanField(default=True)
    fecha = models.DateTimeField(default=timezone.now)

    image = models.ImageField(upload_to='contenido/images', null=True, blank=True)
    video = models.ImageField(upload_to='contenido/videos', blank=True, storage=VideoMediaCloudinaryStorage(),
                              validators=[validate_video])

    ESTADO_CHOICES = (
        ('borrador', 'Borrador'), 
        ('revision', 'En revisión'),
        ('rechazado', 'Rechazado'),
        ('publicado', 'Publicado'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='En revisión')
    
    reportado = models.BooleanField(default=False)

    
    def __str__(self):
        return self.titulo

class Like(models.Model):
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Like de {self.user.username} a {self.contenido.titulo}'