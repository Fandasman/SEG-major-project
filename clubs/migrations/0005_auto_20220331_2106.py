# Generated by Django 3.2.5 on 2022-03-31 21:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0004_auto_20220331_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booksratings',
            name='rating',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Accept'), ('R', 'Reject')], default='P', max_length=1),
        ),
    ]
