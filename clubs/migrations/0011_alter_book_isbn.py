# Generated by Django 3.2.5 on 2022-02-05 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0010_alter_book_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]