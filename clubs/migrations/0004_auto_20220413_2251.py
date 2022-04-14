# Generated by Django 3.2.5 on 2022-04-13 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0003_alter_invitation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('R', 'Reject'), ('A', 'Accept')], default='P', max_length=1),
        ),
    ]