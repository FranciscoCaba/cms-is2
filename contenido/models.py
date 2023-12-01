from django.db import models
from django.contrib.auth.models import User,Permission
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.urls import reverse_lazy
from django.utils.text import Truncator
from django.core.files.storage import default_storage 
from cloudinary_storage.storage import VideoMediaCloudinaryStorage, RawMediaCloudinaryStorage
from cloudinary_storage.validators import validate_video
from django.db.models import Avg

# Create your models here.
class Categoria(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=True)
    nombre = models.CharField(max_length=50)
    moderada = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    seguidores=models.ManyToManyField(User,through='Favoritos',related_name='categoria_favoritos')

    def __str__(self):
        return self.nombre
    
class Contenido(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='categoria', verbose_name='Categoria',default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuario', verbose_name='Usuario')
    titulo = models.CharField(max_length=100)
    resumen = models.CharField(max_length=250, default = '')
    descripcion = RichTextUploadingField(null=True,config_name='default')
    likes = models.ManyToManyField(User, through='Like', related_name='contenido_likes')
    dislikes = models.ManyToManyField(User, through='Dislike', related_name='contenido_dislikes')
    is_active = models.BooleanField(default=True)
    fecha = models.DateTimeField(default=timezone.now)
    solo_suscriptores = models.BooleanField(default=False)
    nota = models.TextField(blank=True, null=True)
    visitas = models.PositiveIntegerField(default=0)
    compartidos = models.IntegerField(default=0)
    destacado = models.BooleanField(default=False)
    promedio_calificacion = models.FloatField(default=0.0)

    ESTADO_CHOICES = (
        ('borrador', 'Borrador'), 
        ('revision', 'En revisión'),
        ('apublicar','A publicar'),
        ('rechazado', 'Rechazado'),
        ('publicado', 'Publicado'),
        ('inactivo', 'Inactivo'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='En revisión')
    
    reportado = models.BooleanField(default=False)
    def obtener_promedio_calificacion(self):
        promedio = self.calificaciones.aggregate(promedio=Avg('estrellas'))['promedio']
        if promedio is None:
            promedio = 'Sin calificaciones'
        else:
            promedio = round(promedio, 3)
        return promedio
    
    def save(self, *args, **kwargs):
        # Guardar una nueva versión de Contenido antes de cada modificación
        super().save(*args)
        if self.obtener_promedio_calificacion() == 'Sin calificaciones':
            self.promedio_calificacion = 0.0
        else:
            self.promedio_calificacion = self.obtener_promedio_calificacion()

    def save_version(self, *args, **kwargs):
        super().save(*args)

        user = kwargs.get('user', None)

        VersionContenido.objects.create(
            contenido=self,
            categoria=self.categoria,
            user_modificacion=user,
            titulo=self.titulo,
            resumen=self.resumen,
            descripcion=self.descripcion,
            estado=self.estado,
            solo_suscriptores = self.solo_suscriptores,
            nota=self.nota,
            version=1  # La primera versión siempre es 1
        )

    def __str__(self):
        return self.titulo
    
    class Meta:
        permissions = [
            ('ver_borradores', 'Ver borradores'),
            ('ver_rechazados', 'Ver rechazados'),
            ('ver_revisiones', 'Ver revisiones'),
            ('ver_a_publicar', 'Ver contenidos a publicar'),
            ('ver_kanban', 'Ver kanban'),
            ('ver_todos_kanban', 'Ver todos kanban'),
            ('puede_publicar_rechazar', 'Puede publicar o rechazar'),
            ('puede_editar_aceptar', 'Puede editar o aceptar'),
            ('ver_todos_borradores', 'Ver todos los borradores'),
            ('puede_publicar_no_moderada', 'Puede publicar en categoria no moderada'),
            ('ver_versiones', 'Ver versiones'),
            ('ver_todos_versiones', 'Ver todos las versiones'),
            ('ver_historial', 'Ver historial'),
            ('puede_calificar', 'Puede calificar'),
            ('puede_inactivar_contenido', 'Puede inactivar contenido'),
            ('puede_destacar_contenido', 'Puede destacar contenido'),
            ('puede_ver_estadisticas', 'Puede ver estadísticas'),
        ]
    
    def get_absolute_url(self, **kwargs):
        return reverse_lazy('detalle_contenido', kwargs={'pk': self.id})

class VersionContenido(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=True)
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE, related_name='versiones', verbose_name='Contenido')
    user_modificacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='categoria_version', verbose_name='Categoria',default=None)
    titulo = models.CharField(max_length=100)
    resumen = models.CharField(max_length=250, default = '')
    descripcion = RichTextUploadingField(null=True,config_name='default')
    estado = models.CharField(max_length=20)
    fecha_modificacion = models.DateTimeField(default=timezone.now)
    version = models.PositiveIntegerField(default=1)
    solo_suscriptores = models.BooleanField(default=False)
    nota = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Determinar la última versión y asignar la siguiente
        last_version = VersionContenido.objects.filter(contenido=self.contenido).order_by('-version').first()
        if last_version:
            self.version = last_version.version + 1
        else:
            self.version = 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Versión {self.version} de {Truncator(self.contenido.titulo).chars(30)}'


class Like(models.Model):
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Like de {self.user.username} a {self.contenido.titulo}'

class Dislike(models.Model):
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Dislike de {self.user.username} a {self.contenido.titulo}'
    
class Image(models.Model):
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='contenido/images', null=True, blank=True)

class Video(models.Model):
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE, related_name='videos')
    video = models.ImageField(upload_to='contenido/videos', null=True,blank=True, storage=VideoMediaCloudinaryStorage(),
                              validators=[validate_video])
class Archivos(models.Model):
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE, related_name='archivos')
    archivo = models.ImageField(upload_to='contenido/archivos', null=True, blank=True,storage=RawMediaCloudinaryStorage())
    
class Comentario(models.Model):
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE, related_name='comentarios')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()

class Favoritos(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Calificacion(models.Model):
    contenido = models.ForeignKey('Contenido', on_delete=models.CASCADE, related_name='calificaciones')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estrellas = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])