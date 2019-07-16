import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SignUpForm, LogInForm, UserUpdateForm, ProfileUpdateForm, PostQuackForm
from django.contrib.auth.models import User
from .models import Quack, Tag
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated:

        posts = Quack.objects.filter(user=request.user)
        liked = [True if post.likes.filter(
            username=request.user).exists() else False for post in posts]

        # To find trending tags
        dict_tags = {}
        all_posts = Quack.objects.all()
        for post in all_posts:
            # print(post.tags, post.content)
            for tag in post.tags.all():
                if tag.name in dict_tags:
                    dict_tags[tag.name] += 1
                else:
                    dict_tags[tag.name] = 0

        trending_tags = [x[0] for x in sorted(
            dict_tags.items(), key=lambda kv: kv[1], reverse=True)]

        if request.method == 'POST':
            post_quack_form = PostQuackForm(request.POST)
            if post_quack_form.is_valid():
                post_quack_form.instance.user = request.user
                tags = []
                tags.extend(
                    list(filter(lambda x: x[0] == '#', post_quack_form.instance.content.split())))
                post_quack_form.save()
                for tag in tags:
                    tag_obj, created = Tag.objects.get_or_create(name=tag)
                    post_quack_form.instance.tags.add(tag_obj)

                return redirect('home')
        else:
            post_quack_form = PostQuackForm()

        return render(request, 'quack/home.html', {'form': post_quack_form, 'zipped_data': zip(posts, liked), 'trending_tags': trending_tags})
    else:
        return render(request, 'quack/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            messages.success(request, f'Your account has been created!')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'quack/signup.html', {'form': form})


@login_required
def profile(request, username):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile', username=request.user.username)
    else:
        if username == request.user.username:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)
            context = {
                'u_form': u_form,
                'p_form': p_form
            }
        else:
            context = {'view_profile': True}

    return render(request, 'quack/profile.html', context)


@require_POST
@login_required
def like(request):
    if request.method == 'POST':
        current_user = request.user
        quack_pk = request.POST.get('pk', None)
        quack = get_object_or_404(Quack, pk=quack_pk)
        if quack.likes.filter(username=current_user).exists():
            quack.likes.remove(current_user)
            message = False
        else:
            quack.likes.add(current_user)
            message = True

    data = {'likes_count': quack.likes_count,
            'liked': message, 'pk': quack_pk}
    return JsonResponse(data)


@login_required
def tag_page(request, tag):
    invalid = False
    posts = Quack.objects.filter(tags__name=tag)
    liked = [True if post.likes.filter(
        username=request.user).exists() else False for post in posts]
    print(len(posts), len(liked))
    if tag[0] != '#':
        posts, liked, invalid = [], [], True
    return render(request, 'quack/tag_page.html', {'zipped_data': zip(posts, liked), 'tag': tag, 'invalid': invalid})


@login_required
@require_GET
def search(request, phrase):
    if phrase[0] == '#':
        phrase = phrase[1:]

    posts = Quack.objects.filter(tags__name__icontains=phrase)
    users = User.objects.filter(username__icontains=phrase)

    data = []
    visited_tags = set()
    for post in posts:
        for tag in post.tags.all():
            if phrase.lower() in tag.name.lower() and tag.name.lower() not in visited_tags:
                data.append(dict([('keyword', tag.name)]))
                visited_tags.add(tag.name.lower())

    for user in users:
        data.append(dict([('keyword', user.username)]))

    return JsonResponse(data, safe=False)
