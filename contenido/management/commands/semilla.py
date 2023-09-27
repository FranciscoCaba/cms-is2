from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from contenido.models import Categoria, Contenido
import lorem  # Esta es una biblioteca para generar texto aleatorio
import random  # Para generar datos aleatorios

class Command(BaseCommand):
    help = 'Carga datos iniciales de Usuarios, Grupos, Categorías y Contenidos'

    
    def generate_random_html_text(self):
        #Genera texto aleatorio con etiquetas HTML aleatorias.
        
        lorem_text = lorem.text()
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

        # Crear grupos
        grupos = ['Suscriptor', 'Autor', 'Editor', 'Publicador', 'Administracion']
        for grupo in grupos:
            Group.objects.get_or_create(name=grupo)

        # Crear usuarios y asignarlos a grupos
        usuarios = {
            'Derlis': 'Suscriptor',
            'Osmani': 'Autor',
            'Fran': 'Editor',
            'Jimmy': 'Publicador'
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

        # Crear categorías
        categorias = ['Deporte', 'Ciencia', 'Cultura', 'Politica', 'Informatica']
        for categoria in categorias:
            Categoria.objects.get_or_create(nombre=categoria, moderada=False, is_active=True)

        # Obtener usuarios
        users = User.objects.all()
        
        # Crear contenidos
        for categoria in Categoria.objects.all():
            for i in range(10):
                titulo = lorem.sentence()

                # Generar descripción en formato HTML aleatorio con etiquetas
                descripcion = self.generate_random_html_text()
                user = users[i] if i < len(users) else users[i % len(users)]
                Contenido.objects.create(
                    categoria=categoria,
                    user=user,
                    titulo=titulo,
                    descripcion=descripcion,
                    is_active=True,
                    estado='Publicado',
                    reportado=False
                )

        self.stdout.write(self.style.SUCCESS('Datos cargados exitosamente.'))