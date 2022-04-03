# Generated by Django 3.2.5 on 2022-03-11 23:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0002_alter_invitation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='maxNumberOfParticipants',
            field=models.PositiveIntegerField(default=16, null=True, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(96)], verbose_name='Maximum Number Of Participants (2 - 96)'),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('R', 'Reject'), ('A', 'Accept')], default='P', max_length=1),
        ),
    ]
