# Generated by Django 5.1.1 on 2025-01-01 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video_game',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]