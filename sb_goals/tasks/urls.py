from django.urls import path
from django.conf.urls import url

from .views import TaskBarChartData, index, detail, done


app_name = 'tasks'

urlpatterns = [
    path('', index, name='index'),
    path('<int:task_id>/', detail, name='detail'),
    path('<int:task_id>/done/', done, name='done'),
    url(r'^api/taskbarchart/data/$', TaskBarChartData.as_view()),
]