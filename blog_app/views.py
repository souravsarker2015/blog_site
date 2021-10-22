from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, PostForm
from .models import Post


# Home page function
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog_app/home.html', {'posts': posts})


# About page function
def about(request):
    return render(request, 'blog_app/about.html')


def contract(request):
    return render(request, 'blog_app/contract.html')


def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        groups = user.groups.all()
        return render(request, 'blog_app/dashboard.html', {'posts': posts, 'full_name': full_name, 'groups': groups})
    else:
        return redirect('login')


def log_in(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Successfully logged in")
                    return redirect('dashboard')
        else:
            form = LoginForm()
        return render(request, 'blog_app/log_in.html', {'form': form})
    else:
        return redirect('dashboard')


def log_out(request):
    logout(request)
    return redirect('home')


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulation!! You have become a author...")
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, 'blog_app/sign_up.html', {'form': form})


# Add new post
def post_add(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'blog_app/add_post.html', {'form': form})
    else:
        return redirect("login")


# Update new post
def post_update(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'blog_app/update_post.html', {'form': form})
    else:
        return redirect("login")


def post_delete(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return redirect('dashboard')
    else:
        return redirect("login")
