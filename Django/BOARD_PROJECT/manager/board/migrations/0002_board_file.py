# Generated by Django 3.2.3 on 2021-05-23 15:17

import board.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=board.models.get_file_path, verbose_name='파일'),
        ),
    ]
