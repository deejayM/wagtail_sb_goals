from django import template
from tasks.models import TaskAction, Task

register = template.Library()


@register.filter(name='write_tasks_done_in_week')
def write_tasks_done_in_week(task):
    """Let's say how many times this task has been none in the last week"""
    seven_day_count = task.how_many_times_has_task_been_done_in_period()
    if seven_day_count == 0:
        return("You haven't done this task in the last week.")
    elif seven_day_count == 1:
        return ("You have done this task once in last week.")
    else:
        return("You have done this task {} times in the last week,".format(seven_day_count))


