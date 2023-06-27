from django.contrib import admin
from .models import UserManager, User, Post, Comment, Like, UserFollows

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserFollows)
admin.site.register(Like)