# Generated by Django 3.0.5 on 2020-06-18 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200618_1221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpage',
            name='author',
        ),
    ]
