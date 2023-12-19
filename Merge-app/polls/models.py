from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.urls import reverse
from django.template.defaultfilters import slugify
import datetime

def create_slug(title): 
    slug = slugify(title)
    qs = Question.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        slug = "%s-%s" %(slug, qs.first().id)
    return slug

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    slug = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.question_text
    
    @admin.display(
            boolean = True,
            ordering = "pub_date",
            description = "Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    def get_absolute_url(self):
        return reverse("detail", kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs): 
      if not self.slug:
          self.slug = create_slug(self.question_text)
      return super().save(*args, **kwargs)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text