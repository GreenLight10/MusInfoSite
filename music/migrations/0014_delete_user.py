# Generated by Django 4.0.4 on 2022-04-25 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0013_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
