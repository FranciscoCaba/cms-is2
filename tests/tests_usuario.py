from django.test import TestCase,Client
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
from app.forms import CustomUserCreationForm, CustomUserChangeForm

# Create your tests here.
class CustomUserFormsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')  

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_register_view_post_valid(self):
        data = {
            'username': 'nuevo_usuario',
            'password1': 'contraseña123',
            'password2': 'contraseña123',
            'email': 'nuevo@usuario.com'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index')) 
        self.assertTrue(get_user_model().objects.filter(username=data['username']).exists())

    def test_custom_user_creation_form(self):
        form_data = {'username': 'testuser','first_name': 'Test','last_name': 'User','email': 'test@example.com',
            'password1': 'testpassword','password2': 'testpassword',}
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid(),"Validacion Fallida")
        user = form.save()
        self.assertEqual(user.username, 'testuser',"Nombre de usuario diferente")
        self.assertEqual(user.first_name, 'Test',"Nombre diferente")
        self.assertEqual(user.last_name, 'User',"Apellido diferente")
        self.assertEqual(user.email, 'test@example.com',"Correo diferente")
        try:
            self.assertTrue(user.check_password('testpassword'))
        except AssertionError as e:
            print("Contrasenha Incorrecta")
        self.assertTrue(user.check_password('testpassword'),"Confirmacion de Contrasenha Incorrecta")
        
    def test_custom_user_change_form(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        form_data = {'username': 'newtestuser','first_name': 'New','last_name': 'User',}
        form = CustomUserChangeForm(instance=user, data=form_data)
        self.assertTrue(form.is_valid(),"Validacion Fallida")
        updated_user = form.save()
        self.assertEqual(updated_user.username, 'newtestuser',"Nombre de usuario incorrecto")
        try:
            self.assertEqual(updated_user.first_name, 'New')
        except AssertionError as e:
            print("Nombre Incorrecto")
        self.assertEqual(updated_user.last_name, 'User',"Apellido incorrecto")
        
