import datetime
import random

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
# from django.core import management # we should check if we actually need this
from django.contrib.auth import get_user_model
from faker import Faker

from tasks.models import TaskAction, Task

class TaskModelTests(TestCase):

    def test_how_many_times_has_task_been_done_in_period_with_future_enddate(self):
        """
        how_many_times_has_task_been_done_in_period returns 0's for future dates
        although this should never happen its still ok.
        """
        future_date = timezone.now() + datetime.timedelta(days=30)
        t = Task()
        self.assertIs(t.how_many_times_has_task_been_done_in_period(7, future_date), 0)

    def sample_create_temp_user(self):
        """Logs in a test user """
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        return user

    def test_new_user_no_tasks(self):
        """If we create a new user when we check for blogs it should be blank """
        user = self.sample_create_temp_user()
        user = User.objects.filter(username='testuser')
        user_id = user[0].id
        tasks_count = Task.objects.filter(user=user_id).count()
        self.assertEqual(tasks_count, 0)


class TaskIndexViewTests(TestCase):
    def test_no_tasks(self):
        """
        If no tasks exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('tasks:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No tasks are available.")


class ModelTests(TestCase):

    def sample_task(task_text = 'Sample Task Text'):
        """Create a Sample Task """
        t = Task(task_text = task_text)
        t.save()
        return t

    def test_task_has_been_created(self):
        """Standard test that creates a new task"""
        t = self.sample_task()
        self.assertTrue(True, Task.objects.filter(task_text = 'Sample Task Text' ))

    def test_task_has_been_done_in_day(self):
        """Here we will check the function how_many_times_has_task_been_done_in_period and that it should return the value '1' """
        t = self.sample_task()
        today = timezone.now()
        t.taskaction_set.create(time_checked=today)
        done_today = t.how_many_times_task_has_been_done_in_day(today)
        self.assertEqual(done_today,1 )

    def test_task_has_been_done_in_day_without_action(self):
        """Here we will check the function how_many_times_has_task_been_done_in_period and that it should return the value '1' """
        t = self.sample_task()
        today = timezone.now()
        done_today = t.how_many_times_task_has_been_done_in_day(today)
        self.assertEqual(done_today,0 )

    def test_task_has_been_done_in_last_week_none(self):
        """Test the function how_many_times_has_task_been_done_in_period.
        When we create a new Task and don't assign a TaskAction then this should return 0"""
        t = self.sample_task()
        today = timezone.now()
        done_today = t.how_many_times_has_task_been_done_in_period(7,today)
        self.assertEqual(done_today,0 )

    def test_task_has_been_done_in_last_week_once(self):
        """Test the function how_many_times_has_task_been_done_in_period.
        When we create a new Task and assign a TaskAction today then this should return 1"""
        t = self.sample_task()
        today = timezone.now()
        t.taskaction_set.create(time_checked=today)
        done_today = t.how_many_times_has_task_been_done_in_period(7,today)
        self.assertEqual(done_today,1 )

    def test_task_has_been_done_in_period_twice(self):
        """Test the function how_many_times_has_task_been_done_in_period.
        When we create a new Task and assign a TaskAction today and yesterday  then this should return 2"""
        t = self.sample_task()
        today = timezone.now()
        yesterday = today - timezone.timedelta(days=1)
        t.taskaction_set.create(time_checked=today)
        t.taskaction_set.create(time_checked=yesterday)
        done_today = t.how_many_times_has_task_been_done_in_period(7,today)
        self.assertEqual(done_today,2 )

    def test_task_has_been_done_in_random_period_random_times(self):
        """This test will select a random time span upto a year ( 365 days ) and no less than 2.
        And then select a random amount of taskAction ( between 3 and the random time span )
        It will then select that amount of random dates.  And test on that
        We'll need to make sure none of those days are exactly the same"""
        rnd_timespan = random.randint(2,365) # the amount of days
        rnd_taskaction_amount = random.randint(3, rnd_timespan)
        i = 1
        taskaction_dates = []
        fake = Faker()
        start_date_str = '-' + str(rnd_timespan) + 'd'
        while i < rnd_taskaction_amount:
            faked_date = fake.date_between(start_date=start_date_str, end_date='today')
            # Check that the date here is not already in our list.
            # Let's just have a look at the faked date variable thats being returned.
            if taskaction_dates.count(faked_date) == 0:
                taskaction_dates.append([str(faked_date)])
                i += 1
        # We should have an array of dates at this point.
        # So lets add all of our dates to the system.
        t = self.sample_task()
        for date in taskaction_dates:
            year,month,day = date[0].split("-")
            tz = timezone.datetime(int(year),int(month),int(day),0,0,0,0)
            t.taskaction_set.create(time_checked=tz)

        today = timezone.now()
        task_done_in_period = t.how_many_times_has_task_been_done_in_period(rnd_timespan,today)
        # I think the test is now working bu the code itself is at fault.  This could be our bug.
        self.assertEqual(task_done_in_period, rnd_taskaction_amount - 1)