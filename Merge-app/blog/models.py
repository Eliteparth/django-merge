from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.html import mark_safe
from django.contrib.auth.models import AbstractUser
from PIL import Image
from autoslug import AutoSlugField

class User(AbstractUser):
    dob = models.DateField(null=True, blank=True)
    mobile = models.PositiveIntegerField(blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    avatar = models.ImageField(default='avatar.jpg', upload_to='profile_avatars')
    def __str__(self):
        return f'{self.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 150 or img.width > 150:
            output_size = (150, 150)
            img.thumbnail(output_size)
            img.save(self.avatar.path)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from="name", unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from="name", unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    category = models.ForeignKey(to=Category, related_name="posts", on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(to=Tag, related_name="posts", blank=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(default='blog.jpg', upload_to='blog_image')
    feature_image = models.ImageField(default='blog.jpg', upload_to='feature_image')
    slug = AutoSlugField(populate_from="title", unique=True, editable=True, always_update=True)
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})
    
    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)
    
    def save(self, *args, **kwargs): 
        return super(Post, self).save(*args, **kwargs)
    
    def preview_image(self):
        return mark_safe('<img src = "{url}" width = "100"/>'.format(
             url = self.image.url
         ))

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    parent=models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return self.body
        
    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)
    
