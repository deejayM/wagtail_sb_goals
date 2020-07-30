import datetime

from django.db import models
from django.utils import timezone
from tasks.models import Task, TaskAction
from blog.models import BlogPage

from users.models import Profile
from wagtail.contrib.modeladmin.options import ModelAdmin
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    def get_context(self, request):
        """Update context - includes passing messages/alerts to our homepage
        TODO do we have a user logged in - Only get results if we have. """
        context = super().get_context(request)
        context['welcome_msg'] = ''

        current_month = int( timezone.now().strftime('%-m') )
        current_year = int( timezone.now().strftime('%Y') )
        current_day = int( timezone.now().strftime('%-d') )

        ta_obj = TaskAction()
        has_ta_been_done_today = ta_obj.have_any_tasks_been_done_on_this_day(current_day, current_month, current_year)
        if not has_ta_been_done_today:
            """ Output a message that no tasks have been done yet today """
            context['welcome_msg'] += "You haven't completed any tasks yet today ! <br><br>"

        blogs = BlogPage.objects.live().order_by('first_published_at')
        blogs_current_user = []
        user_id = request.user.id
        for blogpage in blogs:
            if blogpage.owner.id == user_id:
                blogs_current_user.append(blogpage)

        context['username'] = request.user.username

        today = datetime.datetime.today()
        if len(blogs_current_user) is not 0:
            last_blog_index = len(blogs_current_user)-1
            last_blog = blogs_current_user[last_blog_index].first_published_at.replace(tzinfo=None) # removed info to make both dates Naive
            delta = today - last_blog

        if len(blogs_current_user) == 0:
            context['welcome_msg'] += 'Time to go surfing and registering it !<br><br>'
        elif delta.days > 5:
            context['welcome_msg'] += 'You haven\'t been surfing for ' + str(delta.days) + ' days.  SORT IT OUT !!! <br><br>'
        elif not delta.days == 0:
            context['welcome_msg'] += 'It has been ' + str(delta.days) + ' days since your last surf <br><br>'
        else:
            context['welcome_msg'] += 'Yewwwww! Hope you  enjoyed your surf :) <br><br>'

        t = Task()
        worst_performer = t.whats_your_worst_performer_in_timespan(request, 'month')

        context['welcome_msg'] += worst_performer

        return context

class CustomMenu(ModelAdmin):

    def get_list_display(self, request):
        """
        Return a sequence containing the fields/method output to be displayed
        in the list view.
        """
        return self.list_display

    list_display = []

