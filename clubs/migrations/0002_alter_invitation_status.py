# Generated by Django 3.2.5 on 2022-03-23 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='status',
            field=models.CharField(choices=[('R', 'Reject'), ('A', 'Accept'), ('P', 'Pending')], default='P', max_length=1),
        ),
    ]
