# Generated by Django 3.2.5 on 2022-03-30 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0009_merge_20220330_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='status',
            field=models.CharField(choices=[('A', 'Accept'), ('P', 'Pending'), ('R', 'Reject')], default='P', max_length=1),
        ),
    ]
