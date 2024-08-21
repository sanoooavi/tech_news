from django.db.models import Count, Q
from rest_framework.response import Response

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from .models import Article
from .serializers import ArticleSerializer


class ArticleListView(GenericAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def get(self, request, *args, **kwargs):
        tag_names = request.query_params.getlist('tags')
        print(
            tag_names
        )
        articles = self.get_queryset()

        # Filter articles that have all the tags in tag_names
        if tag_names:
            # articles = articles.filter(tags__name__in=tag_names)
            articles = articles.annotate(num_tags=Count('tags', filter=Q(tags__name__in=tag_names)))
            articles = articles.filter(num_tags=len(tag_names))
        ser = self.serializer_class(articles, many=True)
        return Response(ser.data)


class ArticleCountView(APIView):
    def get(self, request, *args, **kwargs):
        count = Article.objects.count()
        return Response({"article_count": count})


class ArticlesByAuthorView(GenericAPIView):
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        author_name = request.query_params.get('author')
        if not author_name:
            return Response({"error": "Author name not provided"}, status=400)

        articles = Article.objects.filter(author=author_name)
        ser = self.serializer_class(articles, many=True)
        return Response(ser.data)
