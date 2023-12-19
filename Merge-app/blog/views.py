from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from .forms import *
import csv

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(parent__isnull=True, active=True)
    total_comments = comments.count()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html',{'post':post,'comments': comments, 'total_comments': total_comments, 'comment_form':comment_form})

def reply_page(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id') 
            parent_id = request.POST.get('parent')  
            post_url = request.POST.get('post_url')  
            reply = form.save(commit=False)
            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()
            return redirect(post_url+'#'+str(reply.id))
    return redirect("/")

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'blog/register.html', {'form': form})
    if request.method == "POST":
        form = RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have registered Successfully')
            login(request, user)
            return redirect('post_list')
        else:
            return render(request, 'blog/register.html', {'form': form})
        
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user = user_form.save()
            user.username = user.username.lower()
            user.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user_detail') 
    else:
        user_form = UserUpdateForm(instance=request.user)

    context = { 'user_form': user_form }

    return render(request, 'blog/profile.html', context)

@login_required
def user_detail(request):
    return render(request, 'blog/user_detail.html')

@login_required
def export_csv(request):
    data = User.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
    writer = csv.writer(response)
    writer.writerow(['username', 'email'])
    for row in data:
        writer.writerow([row.username, row.email])
    return response

def list_posts_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)
    context = {"category_name": category.name, "posts": posts}
    return render(request, "blog/post_list.html", context)

def list_posts_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)
    context = {"tag_name": tag.name, "posts": posts}
    return render(request, "blog/post_list.html", context)

def list_all_category(request):
    categories = Category.objects.all()
    return render(request, 'blog/category.html', {'categories': categories})

def list_all_tag(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tag.html', {'tags': tags})