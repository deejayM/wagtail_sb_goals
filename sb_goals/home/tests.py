import datetime
import random

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.test import Client
# from django.core import management # we should check if we actually need this
from django.contrib.auth import get_user_model
from faker import Faker

from tasks.models import TaskAction, Task


class TaskModelTests(TestCase):

    def test_front_page_not_logged_in(self):
        """If we're not logged in we should see a Please login message
        TODO this test isn't working.  We need to find Why text isn't finding in Contains """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    #    self.assertContains(response, "Please login")

    def test_count_days_since_last_surf_check(self):
        """We'd need to spin some fake data and use our code to count. """

        self.assertEqual(0,1)