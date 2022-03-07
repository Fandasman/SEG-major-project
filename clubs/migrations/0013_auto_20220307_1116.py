# Generated by Django 3.2.5 on 2022-03-07 11:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0012_alter_invitation_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpost',
            name='join',
        ),
        migrations.AddField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='EventPost',
        ),
    ]
