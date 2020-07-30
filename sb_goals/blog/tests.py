from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from tasks.models import TaskAction, Task
from blog.models import BlogPage


class BlogModelTests(TestCase):

    def sample_create_temp_user(self):
        """Logs in a test user """
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        return user

    def test_new_user_no_blogs(self):
        """If we create a new user when we check for blogs it should be blank """
        user = self.sample_create_temp_user()
        user = User.objects.filter(username='testuser')
        user_id = user[0].id
        blogs_count = BlogPage.objects.filter(owner=user_id).count()
        self.assertEqual(blogs_count, 0)

