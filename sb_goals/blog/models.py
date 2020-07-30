import datetime
import calendar

from django.db import models
from django.shortcuts import render
from django.utils import timezone
from django.conf import settings
from wagtail.contrib.modeladmin.options import ModelAdmin

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable, PageRevision
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    ObjectList,
    TabbedInterface
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from blog.views import days_in_month


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('first_published_at')
        blogpages_current_user = []
        for blogpage in blogpages:
            if blogpage.owner.id == request.user.id:
                blogpages_current_user.append(blogpage)

        context['blogpages'] = blogpages_current_user
        return context

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]


class BlogPageRevision(PageRevision):

    def publish(self):
        """Do nothing"""
        return


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    # TODO it'd be cool to make this show for SuperUsers Only
    promote_panels = []
    settings_panels = []

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading='My Surf')
        ]
    )

    def how_many_days_since_last_post(self) -> int:
        """Returns how many days since the last post
         TODO NOT WORKING possible issue with SELF. """
        blogs = self.objects.live().order_by('last_published_at')
        today = datetime.datetime.today()
        last_blog_index = len(blogs) - 1
        last_blog = blogs[last_blog_index].last_published_at.replace(
            tzinfo=None)  # removed info to make both dates Naive
        delta = today - last_blog

        return delta.days

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class BlogPageCalendar(Page):

    def get_context(self, request, *args, **kwargs):
        """This will  give us a list of block posts in our contexts, that we can then add to the calendar that we'll create with bootcamp.  """
        context = super().get_context(request)
        current_month = int(timezone.now().strftime('%-m'))
        if request.GET.get('month', ''):
            month_number = int(request.GET.get('month', ''))
        else:
            month_number = current_month

        context['month'] = calendar.month_name[month_number]
        current_day = timezone.now().strftime('%-d')
        current_year = timezone.now().strftime('%Y')
        days_in_current_month = days_in_month(2020, 6) + 1
        list_of_days = [*range(1, days_in_current_month)]
        days_output = []
        # TODO make Blog listing pages to send to
        for day in list_of_days:
            # get  Queryset for the day
            # we should probably send through array that get's processed in the template.
            blogs_today = BlogPage.objects.filter(first_published_at__year=current_year,
                                                  first_published_at__month=month_number, first_published_at__day=day,
                                                  owner=request.user.id)
            # this give us the title of the first item  blogs_today[0].title
            # can we create a day view list and view that instead.
            if blogs_today:
                day_list = '<p><a href="' + str(blogs_today[0].url_path.replace("/home", '')) + '">' + str(
                    blogs_today[0].title) + '</a></p>'  # lets
            else:
                day_list = ''
            if (int(day) == int(current_day)) & (month_number == current_month):
                days_output.append('<span class="active" >' + str(day) + '</span>' + str(day_list))
            else:
                days_output.append(str(day) + day_list)

        if month_number == current_month:
            context['this_month'] = True
        else:
            context['this_month'] = False
        context[
            'prev_month'] = month_number - 1  # we'll need to check for when we get to zero - maybe 'calendar' has a tool
        context[
            'next_month'] = month_number + 1  # we'll need to check for when we get to 12 - maybe 'calendar' has a tool
        context['day_output'] = days_output
        # Add a start day offset!
        context['day_number_start'] = calendar.weekday(2020, month_number, 1)
        context['hello_world'] = 'Hello World'

        return context
