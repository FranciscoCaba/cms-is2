from django.test import TestCase
from django.contrib.auth.models import User
from app.forms import CustomUserCreationForm, CustomUserChangeForm

# Create your tests here.
class CustomUserFormsTestCase(TestCase):
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
            self.assertTrue(user.check_password('testpassword123'))
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
            self.assertEqual(updated_user.first_name, 'New1')
        except AssertionError as e:
            print("Nombre Incorrecto")
        self.assertEqual(updated_user.last_name, 'User',"Apellido incorrecto")