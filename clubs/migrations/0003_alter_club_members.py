# Generated by Django 3.2.5 on 2022-02-11 17:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0002_auto_20220211_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='member', to=settings.AUTH_USER_MODEL),
        ),
    ]
