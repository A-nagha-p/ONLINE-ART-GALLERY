
from django.contrib import admin
from django.urls import path
from.import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.index,name="home"),
    path('index.html',views.index,name="home"),
    path('login.html',views.login,name="login"),
    path('register.html',views.register,name="register"),
    path('blog.html',views.blog,name="blog"),
    path('about.html',views.about,name="about"),
    path('contact.html',views.contact,name="contact"),
    path('exhibition.html',views.exhibition,name="exhibition"),
    path('competition.html',views.competition,name="competition"),
    path('artstore.html',views.artstore,name="artstore"),
    path('index',views.index,name="index"),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    
]
