from django.contrib import admin
from .models import BlogPost

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_on', 'is_active')
    search_fields = ('title', 'author__username')

admin.site.register(BlogPost, BlogAdmin)