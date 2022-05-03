from time import time
from django.utils.text import slugify
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


def gen_slug(sl):
    new_slug = slugify(sl)
    return new_slug + '-' + str(int(time()))

def upload_gallery_image(instance, filename):
    return f"images/artists/{instance.artist.name}/gallery/{filename}"

def upload_post_image(instance, filename):
    return f"images/users/{instance.title}/post image/{filename}"

def upload_profile_image(instance, filename):
    return f"images/users/{instance.user.username}/avatar/{filename}"

class Comment(models.Model):
    post_name = models.ForeignKey(
        'Post', null=True, on_delete=models.CASCADE, related_name='comments')
    comm_name = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.comm_name = slugify(
            "comment by" + "-" + str(self.author) + str(self.date_added))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name

    class Meta:
        ordering = ['date_added']


class Reply(models.Model):
    comment_name = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='replies')
    reply_body = models.TextField(
        max_length=500, verbose_name='ответ на комментарий')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "reply to " + str(self.comment_name.comm_name)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Фамилия')
    email = models.EmailField(null=True, blank=True, verbose_name='Адрес электронной почты')
    avatar = models.ImageField(upload_to=upload_profile_image, default='images/users/default-avatar.png', verbose_name='Аватар')
    
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class Member(models.Model):
    """Музыкант"""
    name = models.CharField(max_length=255, verbose_name='Имя музыканта')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Музыкант'
        verbose_name_plural = 'Музыканты'



class Genre(models.Model):
    """Музыкальный жанр"""
    name = models.CharField(max_length=50, verbose_name='Название жанра')
    slug = models.SlugField(unique=True, db_index=True)
    description = models.TextField(verbose_name='Описание', default='Описание появится позже')
    image = models.ImageField(upload_to='images/genres/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Album(models.Model):
    """Альбом"""
    name = models.CharField(max_length=255, verbose_name='Название альбома')
    release_date = models.CharField(max_length=4, verbose_name='Дата релиза')
    slug = models.SlugField()
    image = models.ImageField(upload_to='images/albums/', null=True, blank=True)
    url = models.CharField(max_length=500, verbose_name='Ссылка на альбом', default="Ссылки нет")

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'


class Artist(models.Model):
    """Исполнитель"""
    name = models.CharField(max_length=255, verbose_name='Исполнитель/группа')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='genresartist')
    albums = models.ManyToManyField(Album, verbose_name='Альбомы', default='На данный момент альбомы не были добавлены на сайт', related_name='albumsartist')
    members = models.ManyToManyField(Member, verbose_name='Участник', related_name='membersartist')
    slug = models.SlugField(unique=True, db_index=True)
    description = models.TextField(verbose_name='Описание', default='Описание появится позже')
    image = models.ImageField(upload_to='images/artists/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"
  
    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'


class News(models.Model):
    """Новости"""
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(max_length=150, default='news')
    anons = models.CharField(max_length=250, verbose_name='Краткое описание')
    description = models.TextField(verbose_name='Текст новости', default='Текст появится позже')
    date = models.DateField(verbose_name='Дата публикации')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
   
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

class CategoryPost(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(verbose_name='Описание категории', default='Текст появится позже')
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name
   
    class Meta:
        verbose_name = 'Категория постов'
        verbose_name_plural = 'Категории постов'

class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Заголовок')
    slug = models.SlugField(max_length=150, blank=True, default='post')
    text = models.TextField(blank=True, db_index=True, verbose_name='Текст')
    image = models.ImageField(upload_to=upload_post_image, null=True, blank=True, verbose_name='Изображение для поста')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Профиль автора', related_name='profilepost')
    category = models.ForeignKey(CategoryPost, on_delete=models.CASCADE, default='', verbose_name='Категория поста', related_name='categorypost')
    date_pub = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    def get_review(self):
        return self.reviews.filter(parent__isnull=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title
   
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-date_pub']

class Image(models.Model):
    image = models.ImageField(upload_to=upload_gallery_image)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="images")



def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)


