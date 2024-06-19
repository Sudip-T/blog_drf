from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')
    list_display = ('email', 'first_name', 'last_name', 'is_superuser')
    # exclude = ('password',)
    
admin.site.register(CustomUser, CustomUserAdmin)