from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response

from tasks.models import TaskAction, Task


class TaskBarChartData(APIView):
    """We'll be return the data for the last 4 weeks for the requested task"""
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        if request.GET.get('task_id'):
            task_id = request.GET.get('task_id')
        else:
            task_id = 1
        labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
        t = Task.objects.get(pk=task_id)
        wk1_date = date.today() - timedelta(21)
        wk2_date = date.today() - timedelta(14)
        wk3_date = date.today() - timedelta(7)
        wk1_count = t.how_many_times_has_task_been_done_in_period(7, wk1_date)
        wk2_count = t.how_many_times_has_task_been_done_in_period(7, wk2_date)
        wk3_count = t.how_many_times_has_task_been_done_in_period(7, wk3_date)
        wk4_count = t.how_many_times_has_task_been_done_in_period()
        data = {
            "labels": labels,
            "default": [wk1_count, wk2_count, wk3_count, wk4_count]
        }
        return Response(data)


def index(request):
    """Lets display our list of tasks"""
    current_user_id = request.user.id
    full_task_list = Task.objects.filter(user=current_user_id)
    template = loader.get_template('tasks/index.html')
    context = {
        'full_task_list': full_task_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/detail.html', {'task': task})


def done(request, task_id):
    """"Marking a task as done will create a new object and save when this task has been marked as done"""
    t = Task.objects.get(pk=task_id)
    t.taskaction_set.create(time_checked=timezone.now())
    return HttpResponseRedirect(reverse('tasks:index'))
