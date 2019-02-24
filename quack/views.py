import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SignUpForm, LogInForm, UserUpdateForm, ProfileUpdateForm, PostQuackForm
from .models import Quack
from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.views.decorators.http import require_POST


def home(request):
    if request.user.is_authenticated:
        posts = Quack.objects.filter(user=request.user)
        liked = [True if post.likes.filter(
            username=request.user).exists() else False for post in posts]
        if request.method == 'POST':
            post_quack_form = PostQuackForm(request.POST)
            if post_quack_form.is_valid():
                post_quack_form.instance.user = request.user
                post_quack_form.instance.tags = " ".join(
                    filter(lambda x: x[0] == '#', post_quack_form.instance.content.split()))
                print(post_quack_form)
                post_quack_form.save()
                return redirect('home')
        else:
            post_quack_form = PostQuackForm()

        return render(request, 'quack/home.html', {'form': post_quack_form, 'zipped_data': zip(posts, liked)})
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
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'quack/signup.html', {'form': form})


def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'quack/profile.html', context)


@require_POST
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

    ctx = {'likes_count': quack.total_likes,
           'liked': message, 'pk': quack_pk}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')
