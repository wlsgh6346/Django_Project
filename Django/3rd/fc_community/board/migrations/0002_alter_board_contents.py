# Generated by Django 3.2.3 on 2021-05-16 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='contents',
            field=models.TextField(verbose_name='내용'),
        ),
    ]
