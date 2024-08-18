from rest_framework.response import Response

from rest_framework.generics import GenericAPIView
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
        if tag_names:
            articles = articles.filter(article_tags__tag__name__in=tag_names).distinct()
        ser = self.serializer_class(articles, many=True)
        return Response(ser.data)
