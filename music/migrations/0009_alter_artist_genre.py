# Generated by Django 4.0.4 on 2022-04-21 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0008_delete_all'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genresartist', to='music.genre'),
        ),
    ]
