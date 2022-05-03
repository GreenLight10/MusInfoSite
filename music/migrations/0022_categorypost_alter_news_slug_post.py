# Generated by Django 4.0.4 on 2022-04-27 14:30

from django.db import migrations, models
import django.db.models.deletion
import music.models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0021_alter_profile_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('slug', models.SlugField(max_length=150, unique=True)),
            ],
            options={
                'verbose_name': 'Категория постов',
                'verbose_name_plural': 'Категории постов',
            },
        ),
        migrations.AlterField(
            model_name='news',
            name='slug',
            field=models.SlugField(max_length=150),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=150, verbose_name='Заголовок')),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
                ('text', models.TextField(blank=True, db_index=True, verbose_name='Текст')),
                ('image', models.ImageField(blank=True, null=True, upload_to=music.models.upload_post_image, verbose_name='Изображение для поста')),
                ('date_pub', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('category', models.ManyToManyField(related_name='categorypost', to='music.categorypost', verbose_name='Категория поста')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profilepost', to='music.profile', verbose_name='Профиль автора')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
            },
        ),
    ]
