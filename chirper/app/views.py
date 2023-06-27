from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, logout
from django.db.models import Q
from django.http import Http404
from .models import User, Post, Comment, Like, UserFollows
from .forms import LoginForm, RegistationForm, LogoutForm, CreatePostForm, SearchForm, CreateCommentForm

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    users = UserFollows.objects.filter(follower=request.user)
    users_list = users.values_list('follows', flat=True)
    posts = Post.objects.filter(Q(author=request.user)|Q(author__in=users_list)).order_by('-publish_date')
    logged_user = request.user
    return render(request,'index.html',{'posts' : posts,'logged_user':logged_user})

def log_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            f_username = form.cleaned_data['username']
            f_password = form.cleaned_data['password']
            if User.objects.filter(username=f_username).exists():
                user = User.objects.get(username=f_username)
                if user.password==f_password:
                    login(request, user)
                    return redirect('index')
            else:
                form.add_error(None, 'Invalid username or password')
    
    else:
        form = LoginForm()
    return render(request,'login.html', {'form': form})

def logout_user(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        form = LogoutForm(request.POST)
        if form.is_valid():
            f_logout = form.cleaned_data['checkbox']
            if f_logout==True:
                logout(request)
                return redirect('login')
            else:
                return redirect('index')
    else:
        form = LogoutForm()
    return render(request,'logout.html', {'form': form})

def registration(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = RegistationForm(request.POST)
        if form.is_valid():
            f_username = form.cleaned_data['username']
            f_email = form.cleaned_data['email']
            f_password_1 = form.cleaned_data['password_1']
            f_password_2 = form.cleaned_data['password_2']
            if User.objects.filter(username=f_username).exists():
                form.add_error(None, 'Username already taken')
            elif User.objects.filter(email=f_email).exists():
                form.add_error(None, 'Account with this email already exists')
            elif len(f_password_1) < 8:
                form.add_error(None, 'Password must have at least 8 characters')
            elif f_password_1 != f_password_2:
                form.add_error(None, 'Passwords are not same')
            else:
                user = User(username=f_username,password=f_password_1,email=f_email)
                user.save()
                login(request, user)
                return redirect('index')
    
    else:
        form = RegistationForm()
    return render(request,'registration.html', {'form': form})

def create_post(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            f_content = form.cleaned_data['content']
            if len(f_content)>0:
                post = Post(content=f_content,author=request.user)
                post.save()
                return redirect('index')
            else:
                return redirect('create_post')
            
    else:
        form = CreatePostForm()
    return render(request,'create_post.html', {'form': form,'logged_user':request.user})

def profile(request,user_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = get_object_or_404(User,pk=user_id)
    posts = Post.objects.filter(author=user).order_by('-publish_date')
    followed = UserFollows.objects.filter(follower=request.user,follows=user).exists()

    return render(request,'profile.html',{'user':user,'posts' : posts,'logged_user':request.user,'followed':followed})

def follow_profile(request,user_id):
    if not request.user.is_authenticated:
        return redirect('login')
    user = get_object_or_404(User,pk=user_id)
    if UserFollows.objects.filter(follower=request.user,follows=user).exists():
        UserFollows.objects.filter(follower=request.user,follows=user).delete()
    else:
        follow = UserFollows(follower=request.user,follows=user)
        follow.save()

    return redirect('profile',user_id=user_id)

def search(request):
    if not request.user.is_authenticated:
        return redirect('login')
    users = []
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            f_username = form.cleaned_data['username']
            users = User.objects.filter(username__icontains=f_username)
            
    else:
        form = SearchForm()
    return render(request,'search.html', {'form': form,'logged_user':request.user,'users':users})

def followers(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')
    user=User.objects.get(id=user_id)
    followers_list = UserFollows.objects.filter(follows=user)
    users = [follower.follower for follower in followers_list]


    return render(request,'followers.html',{'logged_user': request.user,'current_user':user_id, 'users': users})

def follows(request,user_id):
    if not request.user.is_authenticated:
        return redirect('login')
    user=User.objects.get(id=user_id)
    followers_list = UserFollows.objects.filter(follower=user)
    users = [follower.follows for follower in followers_list]

    return render(request,'followers.html',{'logged_user': request.user,'current_user': user_id, 'users': users})

def comments(request,post_id):
    if not request.user.is_authenticated:
        return redirect('login')
    post = get_object_or_404(Post,pk=post_id)
    liked =  Like.objects.filter(user=request.user,post=post).exists()
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            f_comment = form.cleaned_data['comment']
            if len(f_comment)>0:
                comment = Comment(content=f_comment,author=request.user,parent_post=post)
                comment.save()
            
    else:
        form = CreateCommentForm()
    comments_list = Comment.objects.filter(author=request.user,parent_comm__isnull=True)
    return render(request,'post_comment.html', {'form': form,'logged_user':request.user,'comments':comments_list,'post':post,'liked':liked})

def comment_comment(request,post_id,comment_id):
    if not request.user.is_authenticated:
        return redirect('login')
    post = get_object_or_404(Post,pk=post_id)
    parent_comment = get_object_or_404(Comment,pk=comment_id)
    if post != parent_comment.parent_post:
        raise Http404()
    
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            f_comment = form.cleaned_data['comment']
            if len(f_comment)>0:
                comment = Comment(content=f_comment,author=request.user,parent_post=post,parent_comm=parent_comment)
                comment.save()
            
    else:
        form = CreateCommentForm()
    comments_list = Comment.objects.filter(author=request.user,parent_comm=parent_comment)
    return render(request,'comment_comment.html', {'form': form,'logged_user':request.user,'parrent_comment':parent_comment,'post':post,'comments':comments_list})

def likes(request,post_id):
    if not request.user.is_authenticated:
        return redirect('login')
    post = get_object_or_404(Post,pk=post_id)

    likes = Like.objects.filter(post=post)
    users = [like.user for like in likes]

    return render(request,'likes.html',{'logged_user': request.user, 'users': users,'post_id': post.id})

def like(request,post_id):
    if not request.user.is_authenticated:
        return redirect('login')
    post = get_object_or_404(Post,pk=post_id)

    if Like.objects.filter(user=request.user,post=post).exists():
        Like.objects.filter(user=request.user,post=post).delete()
    else:
        like = Like(user=request.user,post=post)
        like.save()

    return redirect('comment',post_id=post.id)
