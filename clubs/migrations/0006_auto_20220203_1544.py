# Generated by Django 3.2.5 on 2022-02-03 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0005_auto_20220203_1511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='description',
        ),
        migrations.RemoveField(
            model_name='book',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='book',
            name='isFranchise',
        ),
        migrations.RemoveField(
            model_name='book',
            name='pages',
        ),
        migrations.RemoveField(
            model_name='book',
            name='rating',
        ),
        migrations.AddField(
            model_name='book',
            name='imgURLLarge',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='imgURLMedium',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='imgURLSmall',
            field=models.URLField(blank=True),
        ),
    ]