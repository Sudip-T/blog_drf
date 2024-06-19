from django.urls import path
from .views import BlogPostListCreate, BlogPostDetail

urlpatterns = [
    path('blogs/', BlogPostListCreate.as_view(), name='post-list'),
    path('blog/<int:pk>/', BlogPostDetail.as_view(), name='post-detail'),
]
