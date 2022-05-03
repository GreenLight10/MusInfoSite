# Generated by Django 4.0 on 2022-04-14 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='slug',
        ),
        migrations.AlterField(
            model_name='artist',
            name='members',
            field=models.ManyToManyField(related_name='artist', to='music.Member', verbose_name='Участник'),
        ),
    ]