from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

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
    likes = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    ESTADO_CHOICES = (
        ('borrador', 'Borrador'),
        ('revision', 'En revisión'),
        ('rechazado', 'Rechazado'),
        ('publicado', 'Publicado'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='En revisión')
    
    def __str__(self):
        return self.titulo
    
