from rest_framework import serializers
from .models import Article, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['title', 'content', 'author', 'tags', 'author', 'url', 'created']

    # def get_tags(self, obj):
    #     tags = Tag.objects.filter(tagged_articles__article=obj)
    #     return TagSerializer(tags, many=True).data
