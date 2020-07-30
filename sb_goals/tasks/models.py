from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Task(models.Model):
    """A description of the Task and the amount of time after it's been checked until it needs doing again. A task will be assigned to a User.
    TODO why do we have admin_user set to Pk=1 - I can no longer see its purpose """
    task_text = models.CharField(max_length=300)
    admin_user = User.objects.get(pk=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#     task_frequency = models.IntegerField(unique=False,default=1)
    def __str__(self):
        return self.task_text
    def has_been_done_recently(self) -> bool:
        """Well add another argument above which will come from TaskAction
            1. Get all the TaskActions task_this
            2. If 0 then return false
            3. If we don't have any that match the filter the current date then its truw
            4. Does that match todays date - if so then TRUE"""
        task_actions = self.taskaction_set.all()
        count = self.taskaction_set.count()
        if count == 0:
            return False
        else:
            now_str = str(timezone.now())
            year_now = now_str[0:4] # TODO replace this with timezone values - i have an example in blogs I believe
            month_now = now_str[5:7] # TODO replace this with timezone values - i have an example in blogs I believe
            day_now = now_str[8:10] # TODO replace this with timezone values - i have an example in blogs I believe
            get_todays_taskactions = self.taskaction_set.filter(time_checked__year=year_now,
                                                                time_checked__month=month_now,
                                                                time_checked__day=day_now)
            gtt_count = get_todays_taskactions.count()
            if gtt_count > 0:
                return True
            else:
                return False
    def how_many_times_task_has_been_done_in_day(self, date) -> int:
        """The date will be a timezone value but in a string .
        At present the result will never be more that 1.  However making this a count makes it future proof"""
        date_string = str(date)
        year = date_string[0:4]
        month = date_string[5:7]
        day = date_string[8:10]
        get_taskactions = self.taskaction_set.filter(time_checked__year=year,
                                                                        time_checked__month=month,
                                                                        time_checked__day=day)
        return get_taskactions.count()


    def how_many_times_has_task_been_done_in_period(self, time_span_day:int=7, end_date=timezone.now()) -> int:
        """The time span will be an amount of days. Let's have a function for 'how many times in a day'
        We can use that function to build a graph as well.
        TODO we'll need make sure it isn't effected by multiple users"""
        i = 0
        task_count = 0
        while time_span_day >= i:
            d = end_date - timezone.timedelta(days=i)
            task_count += self.how_many_times_task_has_been_done_in_day(d)
            i += 1
        return task_count

    def whats_your_worst_performer_in_timespan(self, request, timespan:str) ->str:
        """This is going to take a timespan. It'll be done for each user.
          Get all of the Task.
          Take a count for each of those tasks in the last whatever period
          Whatever the worst one is then send back a string with what it is and how many times it  has been  done.
          TODO in shell how can we iterate through our tasks getting the TaskActions for each  one"""
        tasks = Task.objects.filter(user=request.user.id)
        task_list = list()
        for task in tasks:
            task_obj = Task.objects.get(pk=task.id)
            task_data = [task.id, task_obj.taskaction_set.all().count()]
            task_list.append(task_data)

        worst_performing_task_title = ''
        worst_performing_task_count = 9999999
        # Now we can iterate thorugh the task_action_list and work out the one with the least.
        for task_check in task_list:
            if task_check[1] < worst_performing_task_count:
                worst_performing_task_title = Task.objects.get(pk=task_check[0]).task_text
                worst_performing_task_count = task_check[1]

        if worst_performing_task_count == 9999999:
            msg = 'in fact, I\'ve just checked and you haven\'t completed any tasks yet at all !!'
        else:
            msg = "The task you've done the least over the last " + timespan + " is '" + str(worst_performing_task_title) + "'. You've only done this " + str(worst_performing_task_count) + ' times.'

                # TODO write a test that checks the above is correct.

        return msg





class TaskAction(models.Model):
     """Note we can collect multiple Task Actions for each Task. We can then add descriptions and extra information to see a log in future."""
     task = models.ForeignKey(Task, on_delete=models.CASCADE)
     time_checked = models.DateTimeField('Time checked off')
     admin_user = User.objects.get(pk=1)
     user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
     def __str__(self):
         return str(self.time_checked)

     def have_any_tasks_been_done_on_this_day(self, day:int, month:int, year:int) -> bool :
         ta = TaskAction.objects.all()
         todays_tas = ta.filter(time_checked__year=year,
                           time_checked__month=month,
                           time_checked__day=day)

         today_ta_count = todays_tas.count()

         if today_ta_count == 0:
             return False
         else:
             return True