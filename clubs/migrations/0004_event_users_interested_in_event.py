# Generated by Django 3.2.5 on 2022-03-12 17:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0003_auto_20220311_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='users_interested_in_event',
            field=models.ManyToManyField(blank=True, related_name='interested_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
