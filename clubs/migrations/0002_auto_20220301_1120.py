# Generated by Django 3.2.5 on 2022-03-01 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booksratings',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='status',
            field=models.CharField(choices=[('A', 'Accept'), ('P', 'Pending'), ('R', 'Reject')], default='P', max_length=1),
        ),
    ]