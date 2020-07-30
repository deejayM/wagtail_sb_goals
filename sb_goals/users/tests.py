from django.test import TestCase

from django.utils import timezone
from django.urls import reverse
from django.test import Client
# from django.core import management # we should check if we actually need this
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from faker import Faker


from tasks.models import TaskAction, Task


class TaskModelTests(TestCase):

    def sample_user_login(self):
        """Logs in a test user """
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        return user

    def test_login_url(self):
        """Does the login page work """
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_register_url(self):
        """Does the login page work """
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        """Does the logout page work - we should be logged in first though """
        user = self.sample_user_login()
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get('/logout/')
        self.assertEqual(response.status_code, 200)