# Generated by Django 4.0.4 on 2022-05-03 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0034_alter_comment_options_alter_post_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='lesson_name',
            new_name='post_name',
        ),
    ]
