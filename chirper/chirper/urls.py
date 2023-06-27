"""
URL configuration for chirper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.log_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('registration/',views.registration,name='registration'),
    path('create_post/',views.create_post,name='create_post'),
    path('profile/<int:user_id>/',views.profile,name='profile'),
    path('follow/<int:user_id>/',views.follow_profile,name='follow'),
    path('search/',views.search,name='search'),
    path('profile/<int:user_id>/followers/',views.followers, name='followers'),
    path('profile/<int:user_id>/follows/',views.followers, name='follows'),
    path('post/<int:post_id>/',views.comments,name='comment'),
    path('post/<int:post_id>/<int:comment_id>',views.comment_comment,name='comment_comment'),
    path('post/<int:post_id>/likes',views.likes,name='likes'),
    path('post/<int:post_id>/like',views.like,name='like'),
]
