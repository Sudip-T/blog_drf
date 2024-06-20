from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='blogs', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_on"]