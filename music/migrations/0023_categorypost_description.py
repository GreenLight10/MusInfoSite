# Generated by Django 4.0.4 on 2022-04-27 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0022_categorypost_alter_news_slug_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorypost',
            name='description',
            field=models.TextField(default='Текст появится позже', verbose_name='Описание категории'),
        ),
    ]