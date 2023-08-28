from django.test import TestCase
from accounts.models import Contenido

# Test de Contenido
class ContenidoTestCase(TestCase):
    def setUp(self):
        Contenido.objects.create(titulo="Hola Mundo", descripcion="Este es un contenido de ejemplo", likes=5)

    def test_contenido(self):
        contenido = Contenido.objects.get(titulo="Hola Mundo")
        self.assertEqual(contenido.get_likes(), 5)