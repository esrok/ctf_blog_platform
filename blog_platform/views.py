from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render


from forms import WriteBlogPostForm
from models import BlogPost


def display_latest_posts(request, count=10):
    if request.user.is_authenticated():
        posts = BlogPost.objects.filter(Q(author=request.user) | Q(private=False))[:count]
    else:
        posts = BlogPost.objects.filter(private=False)[:count]
        
    return render(request, 'display_posts.html', {
        'posts': posts,
        'title': 'Latest posts'
    })


def display_post(request, author, slug):
    post = BlogPost.objects.get(
        author__username=author,
        # slug=slug,
        private=False,
    )
    return render(request, 'display_post.html', {
        'post': post,
        'title': 'My posts',
    })


@login_required
def display_user_posts(request):
    posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'display_posts.html', {
        'posts': posts,
        'title': 'My posts',
    })


def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")

    return render(request, 'accounts/register.html', {
        'form': form,
    })


def login(request):
    auth_form = AuthenticationForm(data=(request.POST or None))
    if request.method == 'POST':
        if auth_form.is_valid():
            auth.login(request, auth_form.get_user())
            return HttpResponseRedirect('/')

    return render(request, 'accounts/login.html', {
        'form': auth_form,
    })


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('blog_platform.views.login'))


@login_required
def write_post(request):
    form = WriteBlogPostForm(request.POST or None, initial={'author': request.user})
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('blog_platform.views.display_user_posts'))
    return render(request, 'write_post.html', {
        'form': form,
        'title': 'Write post',
    })