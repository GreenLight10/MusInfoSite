# Generated by Django 4.0.4 on 2022-04-27 00:47

from django.db import migrations, models
import music.models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0020_profile_email_profile_first_name_profile_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='images/users/default-avatar.png', upload_to=music.models.upload_profile_image, verbose_name='Аватар'),
        ),
    ]
