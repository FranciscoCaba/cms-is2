from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from contenido.models import Categoria, Contenido, Like, Dislike, Calificacion
import lorem  # Esta es una biblioteca para generar texto aleatorio
import random  # Para generar datos aleatorios
from django.db.models import Q
class Command(BaseCommand):
    help = 'Carga datos iniciales de Usuarios, Grupos, Categorías y Contenidos'

    
    def generate_random_html_text(self):
        #Genera texto aleatorio con etiquetas HTML aleatorias.
        
        lorem_text = ' '.join([lorem.sentence() for _ in range(6)])
        # Agregar etiquetas HTML aleatorias
        tags = ['<h1>', '</h1>', '<h2>', '</h2>', '<h3>', '</h3>', '<u>', '</u>', '<br>', '<br/>']
        random_tags = [random.choice(tags) for _ in range(3)]
        random_positions = random.sample(range(len(lorem_text)), len(random_tags))
        random_positions.sort()
        result = []
        prev_pos = 0
        for i, pos in enumerate(random_positions):
            result.append(lorem_text[prev_pos:pos])
            result.append(random_tags[i])
            if not random_tags[i].startswith('</'):
                # Si no es una etiqueta de cierre, añadir un contenido aleatorio
                result.append(lorem.text())
                # Cerrar la etiqueta
                result.append(random_tags[i].replace('<', '</', 1))
            prev_pos = pos
        result.append(lorem_text[prev_pos:])
        return ''.join(result)

    def handle(self, *args, **kwargs):
        self.stdout.write('Cargando datos iniciales...')

        # Obtener permisos
        permisos = Permission.objects.all()

        # Crear grupos
        grupos = ['Suscriptor', 'Autor', 'Editor', 'Publicador', 'Administracion']
        for grupo in grupos:
            Group.objects.get_or_create(name=grupo)
        
        administracion = Group.objects.get(name='Administracion')
        for permiso in permisos:
            administracion.permissions.add(permiso)

        autor = Group.objects.get(name='Autor')
        autor.permissions.add(Permission.objects.get(codename='add_contenido'))
        autor.permissions.add(Permission.objects.get(codename='ver_kanban'))
        autor.permissions.add(Permission.objects.get(codename='ver_borradores'))
        autor.permissions.add(Permission.objects.get(codename='ver_rechazados'))
        autor.permissions.add(Permission.objects.get(codename='ver_versiones'))


        editor = Group.objects.get(name='Editor')
        editor.permissions.add(Permission.objects.get(codename='ver_revisiones'))
        editor.permissions.add(Permission.objects.get(codename='puede_editar_aceptar'))
        editor.permissions.add(Permission.objects.get(codename='ver_todos_kanban'))
        editor.permissions.add(Permission.objects.get(codename='ver_versiones'))
        editor.permissions.add(Permission.objects.get(codename='ver_todos_versiones'))

        publicador = Group.objects.get(name='Publicador')
        publicador.permissions.add(Permission.objects.get(codename='ver_a_publicar'))
        publicador.permissions.add(Permission.objects.get(codename='puede_publicar_rechazar'))
        publicador.permissions.add(Permission.objects.get(codename='ver_todos_kanban'))
        publicador.permissions.add(Permission.objects.get(codename='ver_versiones'))
        publicador.permissions.add(Permission.objects.get(codename='ver_todos_versiones'))
        publicador.permissions.add(Permission.objects.get(codename='puede_ver_estadisticas'))
        

        # Crear usuarios y asignarlos a grupos
        usuarios = {
            'Derlis': 'Suscriptor',
            'Osmani': 'Autor',
            'Fran': 'Editor',
            'Jimmy': 'Publicador',
            'admin': 'Administracion'
        }

        for nombre_usuario, nombre_grupo in usuarios.items():
            username = nombre_usuario.lower()
            email = f'{username}@email.com'
            password = '123'
            
            user, created = User.objects.get_or_create(username=username, email=email)
            user.set_password(password)
            user.save()
            
            grupo = Group.objects.get(name=nombre_grupo)
            user.groups.add(grupo)

        fran = User.objects.get(username='fran')
        fran.user_permissions.add(Permission.objects.get(codename='puede_publicar_no_moderada'))

        # Crear categorías
        categorias = ['Deporte', 'Ciencia', 'Cultura', 'Politica', 'Informatica']
        for categoria in categorias:
            Categoria.objects.get_or_create(nombre=categoria, moderada=False, is_active=True)

        # Obtener usuarios
        users = User.objects.all()
        
        # Crear contenidos
        for categoria in Categoria.objects.all():
            for i in range(4):
                titulo = lorem.sentence()
                resumen = ' '.join([lorem.sentence() for _ in range(3)])
                # Generar descripción en formato HTML aleatorio con etiquetas
                descripcion = self.generate_random_html_text()
                user = users[i] if i < len(users) else users[i % len(users)]
                Contenido.objects.create(
                    categoria=categoria,
                    user=user,
                    titulo=titulo,
                    resumen=resumen,
                    descripcion=descripcion,
                    is_active=True,
                    estado='Publicado',
                    reportado=False
                )
        
        # Interacciones aleatorias
        contenidos = Contenido.objects.all()
        for contenido in contenidos:
            for user in users:
                # Likes y dislikes
                roll = random.randint(0, 2)
                if roll == 1:
                    Like.objects.create(contenido=contenido, user=user)
                elif roll == 2:
                    Dislike.objects.create(contenido=contenido, user=user)
                else:
                    pass

                # Calificaciones
                roll = random.randint(1, 5)
                roll2 = random.randint(0, 1)
                if roll2 == 1:
                    Calificacion.objects.create(contenido=contenido, usuario=user, estrellas=roll)
            # Visitas
            contenido.visitas = random.randint(0, 1000)
            contenido.compartidos = random.randint(0, 10)
            contenido.save()

        self.stdout.write(self.style.SUCCESS('Datos cargados exitosamente.'))