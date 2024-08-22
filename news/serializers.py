from rest_framework import serializers
from .models import Article, Tag


class TagSerializer(serializers.ModelSerializer):
    """
       A simple serializer for tags. Just grabs everything from the Tag model.
    """
    class Meta:
        model = Tag
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    """
        Serializer for articles. It includes the tags as nested objects and pulls in all the important article details.

        Attributes:
            tags (TagSerializer): A nested serializer for tags related to the article.
    """
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['title', 'content', 'author', 'tags', 'author', 'url', 'created']

