from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'category', 'tags', 'image', 'feature_image')
        #category = forms.ModelChoiceField(queryset=models.Category.objects.all(), widget=forms.RadioSelect)

class RegisterForm(UserCreationForm):
    avatar = models.ImageField(default='avatar.jpg', upload_to='profile_avatars')
    # mobile = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'type': 'number'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'dob', 'mobile', 'address', 'city', 'country','avatar']
        widgets = {
            'dob': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)'}
            )
        }
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'avatar', 'mobile', 'address', 'city', 'country']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment    
        fields = ('name', 'body')