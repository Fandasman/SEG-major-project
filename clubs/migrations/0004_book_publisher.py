# Generated by Django 3.2.5 on 2022-02-01 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0003_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.CharField(default='', max_length=100),
        ),
    ]
