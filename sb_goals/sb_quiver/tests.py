from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

class SB_QuiverModelTests(TestCase):

    def sample_user_login(self):
            """Logs in a test user """
            user = User.objects.create(username='testuser')
            user.set_password('12345')
            user.save()
            return user

    def test_does_homepage_exist_logged_in(self):
        """A check on the SB Quiver landing page."""
        user = self.sample_user_login()
        c = Client()
        c.login(username='testuser', password='12345')
        response = c.get('/sb_quiver/')
        self.assertEqual(response.status_code, 200)




