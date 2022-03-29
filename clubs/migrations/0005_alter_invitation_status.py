# Generated by Django 3.2.5 on 2022-03-22 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0004_alter_invitation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='status',
            field=models.CharField(choices=[('A', 'Accept'), ('R', 'Reject'), ('P', 'Pending')], default='P', max_length=1),
        ),
    ]
