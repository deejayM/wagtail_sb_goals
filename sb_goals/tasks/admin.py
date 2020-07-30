from django.contrib import admin

from .models import Task


# class TaskAdmin(admin.ModelAdmin):
#
#     list_display = ('task_text', 'author')
#

admin.site.register(Task)