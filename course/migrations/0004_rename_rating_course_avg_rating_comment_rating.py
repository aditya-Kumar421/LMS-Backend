# Generated by Django 5.0.8 on 2024-08-11 13:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_comment_delete_feedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='rating',
            new_name='avg_rating',
        ),
        migrations.AddField(
            model_name='comment',
            name='rating',
            field=models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
    ]