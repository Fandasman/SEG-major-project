# Generated by Django 3.2.5 on 2022-03-30 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0007_auto_20220314_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='status',
            field=models.CharField(choices=[('R', 'Reject'), ('P', 'Pending'), ('A', 'Accept')], default='P', max_length=1),
        ),
    ]