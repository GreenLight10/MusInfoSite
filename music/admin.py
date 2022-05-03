from django.contrib import admin

from music.models import *

# Register your models here.
admin.site.register(Genre)
admin.site.register(Member)

admin.site.register(Album)
admin.site.register(News)
admin.site.register(Profile)
admin.site.register(CategoryPost)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)

class MembersInline(admin.TabularInline):
    model = Artist.members.through

class AlbumsInline(admin.TabularInline):
    model = Artist.albums.through

class ImageInline(admin.TabularInline):
    model = Image


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):

    inlines = [MembersInline, AlbumsInline, ImageInline,]
    exclude = ('members', 'albums',)



