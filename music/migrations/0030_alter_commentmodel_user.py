# Generated by Django 4.0.4 on 2022-05-02 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0029_alter_commentmodel_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='music.profile'),
        ),
    ]
