
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
    path('exhibition.html',views.product_list,name="exhibition"),
    path('competition.html',views.competition,name="competition"),
    path('artstore.html',views.artstore,name="artstore"),
    path('index',views.index,name="index"),
    path('userprofile.html',views.userprofile,name="userprofile"),
    path('artistprofile.html',views.artistprofile,name="artistprofile"),
    path('admindash.html',views.admindash,name="admindash"),

    path('blogone.html',views.blogone,name="blogone"),
    path('compapply.html',views.compapply,name="compapply"),

    path('addproduct.html',views.add_product,name="addproduct"),
    path('blogupload.html',views.blogupload,name="blogupload"),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('accounts/login/', views.login, name='login'),
    path('logout/',views.logout,name="logout"),

    path('editprofile/', views.editprofile, name='editprofile'),

    path('regusers.html',views.regusers,name="regusers"),
    path('regartist.html',views.regartist,name="regartist"),


    path('viewproduct.html',views.viewproduct,name="viewproduct"),
    

    path('base.html',views.base,name="base"),

    path('product/<int:id>/', views.product_details, name='product_details'),


    

    path('addcompetition.html', views.add_competition, name='add_competition'),

    path('competitions/', views.competition, name='competition'),


    path('viewcompetition.html',views.viewcompetition,name="viewcompetition"),

   
    



    

]
