from .models import BlogPost
from .utility import IsOwnerOrReadOnly
from .serializers import BlogPostSerializer
from rest_framework import generics, permissions


class BlogPostListCreate(generics.ListCreateAPIView):
    '''
    GET: Retrieves a list of blog posts.
    POST: Creates a new blog post with the authenticated user as the author.

    Override method:
    perform_create: Sets the author of the new blog post to the requesting user.
    '''
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogPostDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    GET: Retrieves the details of a specific blog post.
    PUT: Updates an existing blog post with the authenticated user as the author.

    Permission classes:
    - IsOwnerOrReadOnly: Allows only the author of the blog post to update or delete it.

    Override method:
    perform_update: Sets the author of the updated blog post to the requesting user.
    '''
    permission_classes = [IsOwnerOrReadOnly]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
