# Generated by Django 5.1.1 on 2024-12-22 18:06

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Plataform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Video_game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('url_inf', models.URLField()),
                ('url_img', models.URLField()),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('score', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)])),
                ('description', models.TextField()),
                ('release_date', models.DateField(null=True)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.developer')),
                ('genres', models.ManyToManyField(to='main.genre')),
                ('plataform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.plataform')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.store')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
