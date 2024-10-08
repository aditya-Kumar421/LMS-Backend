# Generated by Django 5.0.8 on 2024-08-11 06:06

import cloudinary.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('price', models.PositiveIntegerField(null=True)),
                ('short_description', models.CharField(blank=True, max_length=200, null=True)),
                ('thumbnail', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_updated', models.DateTimeField(auto_now=True)),
                ('review_count', models.PositiveIntegerField(default=0, null=True)),
                ('rating', models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latest_review', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('user', models.CharField(default=' ', max_length=200)),
                ('comment', models.TextField(blank=True, default=' ', null=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_name', models.TextField(max_length=200, null=True)),
                ('length', models.CharField(default='', max_length=100)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('time_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('sector_image', cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='image')),
            ],
        ),
    ]
