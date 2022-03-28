# Generated by Django 3.2.5 on 2022-03-28 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0005_alter_invitation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Accept'), ('R', 'Reject')], default='P', max_length=1),
        ),
    ]
