# Generated by Django 3.0.5 on 2021-10-11 16:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0009_auto_20201006_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='people_who_answered',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
