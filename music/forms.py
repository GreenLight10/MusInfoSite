from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from music.models import *

from django.core.files.images import get_image_dimensions

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'avatar']
        
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)
            if w and h is not None:

                #validate dimensions
                max_width = max_height = 5000
                if w > max_width or h > max_height:
                    raise forms.ValidationError(
                        u'Используйте изображение с разрешением '
                         '%s x %s пикселей или меньше.' % (max_width, max_height))

                if w != h:
                    raise forms.ValidationError(
                        u'Ширина и высота изображения не равны '
                         '(%s x %s).' % (w, h))
    
                #validate content type
                main, sub = avatar.content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                    raise forms.ValidationError(u'Используйте формат файла JPEG, '
                        'GIF или PNG.')
    
                #validate file size
                if len(avatar) > (2000 * 1024):
                    raise forms.ValidationError(
                        u'Размер изрбражения не должен превышать 2000k.')
    
        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        labels = {"body": "Комментарий:"}

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 70, 'placeholder': "Ваш комментарий"}),
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('reply_body',)

        widgets = {
            'reply_body': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'cols': 10}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ReplyForm, self).__init__(*args, **kwargs)