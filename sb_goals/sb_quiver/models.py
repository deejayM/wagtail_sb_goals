from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image



class Board(models.Model):
    """Let's store our measurements in cm's for now.  """
    title = models.CharField(max_length=100)
    image = models.ImageField(default='default-sb.jpg', upload_to='surfboard_pics')
    notes = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    length = models.FloatField(max_length=5, help_text="Enter in 'cm's")
    width = models.FloatField(max_length=5, help_text="Enter in 'cm's")
    thickness = models.FloatField(max_length=5, default=5, help_text="Enter in 'cm's")
    volume = models.FloatField(max_length=5, null=True, blank=True, help_text="Enter in 'millilitres's.  A calculation will be made for you if you fill in L x W x T" )
    wave_range_start = models.FloatField(max_length=5, null=True, blank=True, help_text="Enter in 'cm's")
    wave_range_end = models.FloatField(max_length=5, null=True, blank=True, help_text="Enter in 'cm's")
    make = models.CharField(max_length=100)
    shaper = models.CharField(max_length=100, null=True, blank=True)
    year = models.CharField(max_length=4, blank=True)

    def __str__(self):
        return f'{self.title} Board'

    def get_absolute_url(self):
        return reverse('sb_quiver:board-detail', kwargs={'pk': self.pk})

#     def save(self, *args, **kwargs):
#         """As we save our Profile we'll check that we're not saving a file that's too large"""
#         super().save(*args, **kwargs)
#
#         if img.height > 800:
#             output_size = (_, 800)
#             img.thumbnail(output_size)
#             img.save(self.image.path)