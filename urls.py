
from django.contrib import admin
from django.urls import path
from.import views
from django.contrib.auth import views as auth_views
from .views import delete_competition

from .views import razorpay

from .views import place_bid

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

    path('adminviewproduct.html',views.adminviewproduct,name="adminviewproduct"),

    path('delete_competition/<int:competition_id>/', delete_competition, name='delete_competition'),


    path('viewblogs.html', views.viewblogs, name='viewblogs'),


    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),

    
    path('payment_success', views.payment_success, name='payment_success'),
    path('payment_success/<int:paymentid>/<int:userid>/<str:amount>/', views.payment_success, name='payment_success'),

   

   path('viewpayment.html',views.viewpayment,name="viewpayment"),

   path('addauction.html',views.addauction,name="addauction"),

   path('addauction.html', views.addauction, name='addauction'),


   path('auction.html',views.auction,name="auction"),


   path('adminauction.html',views.adminauction,name="adminauction"),

   path('editdateandtime.html',views.editdateandtime,name="editdateandtime"),

   path('auction-product/<int:product_id>/', views.auction_product_detail, name='auction_product_detail'),

   
   path('place_bid/<int:product_id>/', views.place_bid, name='place_bid'),


   path('auctionwinner.html',views.auctionwinner,name="auctionwinner"),



   path('watermark.html',views.watermark,name="watermark"),


   path('adminauctiondelete.html',views.adminauctiondelete,name="adminauctiondelete"),




   path('water.html', views.water, name='water'),  # Changed from '' to 'water/'
   path('upload/', views.upload_image, name='upload_image'),
   path('download/<str:filename>/', views.download_image, name='download_image'),
   



    

]
