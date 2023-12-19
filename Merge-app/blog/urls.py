from django.urls import path
from . import views

urlpatterns = [
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/add_post/', views.post_new, name='post_new'),
    path('comment/reply/', views.reply_page, name="reply"),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path("category/<slug:slug>", views.list_posts_by_category, name="category"),
    path("tag/<slug:slug>", views.list_posts_by_tag, name="post_tag"),
    path('register/', views.sign_up, name='register'),
    path('export-csv/', views.export_csv, name='export_csv'),
    path('category/', views.list_all_category, name='list_of_category'),
    path('tag/', views.list_all_tag, name='list_of_tag'),
    path("user_detail/", views.user_detail, name="user_detail"),
    path('profile/', views.profile, name='profile'),
    path('', views.post_list, name='post_list'),
]