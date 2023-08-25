from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile


class AnimalTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password"
        )
        self.profile = Profile.objects.create(user=self.user)

    def test_profile(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user, self.user)