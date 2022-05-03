from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from music.models import *

from django.views.generic import (DetailView,
                                   FormView,)

from .forms import *

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# from .forms import *
from .models import *
# Create your views here.

def base(request):
    import random
    genres = random.sample(list(Genre.objects.all()), 4)
    artists = random.sample(list(Artist.objects.all()), 4)
    context = {
        'genres': genres,
        'artists': artists,
    }
    return render(request, 'base.html', context)

def genres(request):
    genres = Genre.objects.all().order_by('name')
    paginator = Paginator(genres, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'genres': genres,
        'page_obj': page_obj,
    }
    
    return render(request, 'genres.html', context)

def genre_detail(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    return render(request, 'genre/genre_detail.html', {"genre":genre})


def artists(request):
    artists = Artist.objects.all().order_by('name')
    paginator = Paginator(artists, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'artists': artists,
        'page_obj': page_obj,
    }

    return render(request, 'artists.html', context)

def artist_detail(request, slug):
    artist = get_object_or_404(Artist, slug=slug)
    return render(request, 'artist/artist_detail.html', {"artist":artist,})

@login_required(login_url='login')
def news(request):
        news = News.objects.all().order_by('-date')
        paginator = Paginator(news, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'news': news,
            'page_obj':page_obj,
        }

        return render(request, 'news.html', context)
    
    
@login_required(login_url='login')
def new_detail(request, slug):
    new = get_object_or_404(News, slug=slug)
    return render(request, 'new/new_detail.html', {"new":new,})

@login_required(login_url='login')
def cat_posts(request):
    form = PostForm()
    user = request.user.id
    profile = Profile.objects.get(user__id=user)
    category = CategoryPost.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post()
            post.title = form.cleaned_data.get('title')
            post.text = form.cleaned_data.get('text')
            post.category = form.cleaned_data.get('category')
            post.image = form.cleaned_data.get('image')
            post.profile = profile
            post.save()
            messages.success(request, 'Пост был успешно добавлен!')
            return redirect('posts')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
    context = {
        'category': category,
        'form': form,
    }
    
    return render(request, 'posts.html', context)



@login_required(login_url='login')
def kabinet(request):
    posts = Post.objects.filter(profile=request.user.profile)
    context = {
        'posts': posts,
    }
    
    return render(request, 'kabinet.html', context)

class PostDetailView(DetailView, FormView):
    context_object_name = 'post'
    model = Post
    template_name = 'posts/post_detail.html'
    form_class = CommentForm
    second_form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(request=self.request)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(request=self.request)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'form'
        else:
            form_class = self.second_form_class
            form_name = 'form2'

        form = self.get_form(form_class)

        if form_name == 'form' and form.is_valid():
            print("comment form is returned")
            return self.form_valid(form)
        elif form_name == 'form2' and form.is_valid():
            print("reply form is returned")
            return self.form2_valid(form)

    def get_success_url(self):
        self.object = self.get_object()
        return reverse_lazy('post_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.post_name = self.object.comments.name
        fm.post_name_id = self.object.id
        fm.save()
        return HttpResponseRedirect(self.get_success_url())

    def form2_valid(self, form):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.author = self.request.user
        fm.comment_name_id = self.request.POST.get('comment.id')
        fm.save()
        return HttpResponseRedirect(self.get_success_url())



@login_required(login_url='login')
def post_detail_cat(request, slug):
    posts = get_object_or_404(CategoryPost, slug=slug)
    return render(request, 'posts/post_detail_cat.html', {"posts":posts,})

def albums(request, slug):
        albums = get_object_or_404(Artist, slug=slug)
        context = {
            'albums': albums,
        }

        return render(request, 'albums.html', context)

def album_detail(request, slug):
    album = get_object_or_404(Album, slug=slug)
    return render(request, 'albums/album_detail.html', {"album":album,})


def artist_genre(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    context = {
            'genre': genre,
        }

    return render(request, 'artists_ganre.html', context)

@login_required(login_url='login')
def profile_editor(request):
    form = ProfileForm(instance=request.user.profile)
    user = request.user.id
    profile = Profile.objects.get(user__id=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.email = form.cleaned_data.get('email')
            avatar = request.POST.get('avatar')
            if avatar is None:
                profile.avatar = form.cleaned_data.get('avatar')
            
            profile.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('profile_editor')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
    	    
    context = {
    	'form':form,
    }    
    return render(request, 'profile_editor.html', context)



def registrationF(request):
    user_form = CreateUserForm()

    if request.method == 'POST':
        user_form = CreateUserForm(data=request.POST)

        if user_form.is_valid() :
            user = user_form.save()
            user.save()

            user = user_form.cleaned_data.get('username')
            messages.success(request, 'Аккаунт с именем ' + user + ' успешно создан')
            return redirect('login')

    context = {'user_form': user_form}
    return render(request, 'registration.html', context)

def loginF(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('base')
        else:
            messages.info(request, 'Логин или пароль введены неверно.')

    context = {}
    return render(request, 'login.html', context)

def logoutF(request):
    logout(request)
    return redirect('login')