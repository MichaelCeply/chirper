from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username',max_length=20)
    password = forms.CharField(label='Password',max_length=50, widget=forms.PasswordInput)

class RegistationForm(forms.Form):
    username = forms.CharField(label='Username',max_length=20)
    email = forms.CharField(label='Email',max_length=50, widget=forms.EmailInput)
    password_1 = forms.CharField(label='Password',max_length=50, widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Password',max_length=50, widget=forms.PasswordInput)

class LogoutForm(forms.Form):
    checkbox = forms.BooleanField(label='Do you really want to log out?',required=False)

class CreatePostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

class SearchForm(forms.Form):
    username = forms.CharField(max_length=20)

class CreateCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)