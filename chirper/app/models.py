from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(username=username)

class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=50)
    email = models.EmailField(unique=True,blank=False, null=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['password','email']

    objects=UserManager()

    def __str__(self):
        return self.username
    
class UserFollows(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    follows = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows')


class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return f'{self.author} {self.publish_date}'

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comm = models.ForeignKey('self', null=True,blank=True, on_delete=models.CASCADE)
    publish_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.author} to  {self.parent_post.author}, {self.publish_date}'
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)