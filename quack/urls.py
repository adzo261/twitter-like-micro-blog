from django.urls import path, re_path
from .forms import LogInForm
from . import views as quack_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', quack_views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='quack/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='quack/logout.html'), name='logout'),
    path('signup/', quack_views.signup, name='signup'),
    path('profile/', quack_views.profile, name='profile'),
    path('profile/<username>', quack_views.profile, name='profile'),
    path('like/', quack_views.like, name='like'),
    path('tags/<tag>', quack_views.tag_page, name='tag_page'),
    path('search/<phrase>', quack_views.search, name='search'),
]
