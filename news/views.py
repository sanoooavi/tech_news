from django.db.models import Count, Q
from rest_framework.response import Response

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from .models import Article
from .serializers import ArticleSerializer


class ArticleListView(GenericAPIView):
    """
       Handles the retrieval of articles, and you can even filter them by tags if you want.

       If you pass in some tags as query parameters, you'll get back articles that have all those tags.
       Otherwise, it just gives you everything.
       """
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def get(self, request, *args, **kwargs):
        """
            Grab the list of articles, and filter by tags if any are provided.

               Args:
                   request (HttpRequest): The request object where the tags might be hiding.
                   *args, **kwargs: Just the usual stuff.

               Returns:
                   Response: A list of articles, possibly filtered by the tags you passed in.
        """
        tag_names = request.query_params.getlist('tags')
        print(
            tag_names
        )
        articles = self.get_queryset()

        # Filter articles that have all the tags in tag_names
        if tag_names:
            articles = articles.annotate(num_tags=Count('tags', filter=Q(tags__name__in=tag_names)))
            articles = articles.filter(num_tags=len(tag_names))
        ser = self.serializer_class(articles, many=True)
        return Response(ser.data)


class ArticleCountView(APIView):
    """
        Just tells you how many articles are in the database.
    """
    def get(self, request, *args, **kwargs):
        count = Article.objects.count()
        return Response({"article_count": count})


class ArticlesByAuthorView(GenericAPIView):
    """
       Fetch articles by a specific author.

       Pass the author's name as a query parameter, and you'll get all articles they've written.
    """
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        """
               Get articles by the specified author.

               Args:
                   request (HttpRequest): The request object with the author's name.
                   *args, **kwargs: The usual extras.

               Returns:
                   Response: A list of articles by the author, or an error if no author is provided.
        """
        author_name = request.query_params.get('author')
        if not author_name:
            return Response({"error": "Author name not provided"}, status=400)

        articles = Article.objects.filter(author=author_name)
        ser = self.serializer_class(articles, many=True)
        return Response(ser.data)
