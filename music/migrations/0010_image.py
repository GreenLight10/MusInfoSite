# Generated by Django 4.0.4 on 2022-04-23 13:43

from django.db import migrations, models
import django.db.models.deletion
import music.models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0009_alter_artist_genre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=music.models.upload_gallery_image)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='music.artist')),
            ],
        ),
    ]
