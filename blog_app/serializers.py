from .models import BlogPost
from rest_framework import serializers


class BlogPostSerializer(serializers.ModelSerializer):
    '''
    Converts BlogPost model instances into JSON representation and vice-versa.
    '''
    class Meta:
        model = BlogPost
        fields = '__all__'
        read_only_fields = ('id', 'author')