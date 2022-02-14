# Generated by Django 3.2.5 on 2022-02-14 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0005_club_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='wishlist',
            field=models.ManyToManyField(blank=True, related_name='wishlist', to='clubs.Book'),
        ),
    ]
