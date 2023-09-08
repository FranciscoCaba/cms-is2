from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

class CreateGroupTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpassword'
        )
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()
        self.permission = Permission.objects.create(
            codename='can_create_group',
            name='Can create group',
            content_type_id=1
        )
        self.client.login(username='admin', password='adminpassword')

    def test_create_group(self):
        response = self.client.get(reverse('create_group'))
        self.assertEqual(response.status_code, 200,'Error al cargar pagina')
        group_data = {
            'name': 'Test Group',
            'permissions': [self.permission.id],  
        }
        response = self.client.post(reverse('create_group'), data=group_data, follow=True)
        self.assertEqual(response.status_code, 200,'Error al cargar pagina')
        self.assertTrue(Group.objects.filter(name='Test Group').exists(),'Rol no existe')

    def tearDown(self):
        self.admin_user.delete()
        self.permission.delete()

class GroupEditTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpassword'
        )
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()
        self.permission = Permission.objects.create(
            codename='can_create_group',
            name='Can create group',
            content_type_id=1
        )
        self.group = Group.objects.create(name='Test Group')
        self.client.login(username='admin', password='adminpassword')

    def test_edit_group(self):
        url = reverse('edit_group', args=[self.group.id])
        updated_data = {
            'name': 'Updated Group Name',
            'permissions': [self.permission.id],  
        }
        response = self.client.post(url, updated_data)
        self.assertEqual(response.status_code, 302,'Error al cargar la pagina')
        updated_group = Group.objects.get(id=self.group.id)
        self.assertEqual(updated_group.name, 'Updated Group Name','Rol no actualizado')
        self.assertTrue(updated_group.permissions.filter(id=self.permission.id).exists(),'Permiso actualizado no existe')

    def tearDown(self):
        self.client.logout()
        self.admin_user.delete()
        self.permission.delete()
        self.group.delete()
       