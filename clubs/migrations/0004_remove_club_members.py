# Generated by Django 3.2.5 on 2022-02-11 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0003_alter_club_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='club',
            name='members',
        ),
    ]