import datetime

from django.test import TestCase

# Create your tests here.
import logging
from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Tag, Article
from .serializers import *

logger = logging.getLogger(__name__)


class ArticleTests(TestCase):
    def setUp(self):
        tag1 = Tag.objects.create(name='science')
        tag2 = Tag.objects.create(name='technology')
        tag3 = Tag.objects.create(name='mobile')
        tag4 = Tag.objects.create(name='car')

        news1 = Article.objects.create(title='title1', content='content1', author='author1',
                                       pub_date=datetime.date(2020, 1, 1))

        news2 = Article.objects.create(title='title2', content='content2', author='author2')

        news3 = Article.objects.create(title='title3', content='content3', author='author3',
                                       pub_date=datetime.date(2020, 1, 1))

        ArticleTag.objects.create(article=news1, tag=tag1)
        ArticleTag.objects.create(article=news2, tag=tag2)
        ArticleTag.objects.create(article=news2, tag=tag3)
        ArticleTag.objects.create(article=news3, tag=tag4)
        ArticleTag.objects.create(article=news1, tag=tag2)
        ArticleTag.objects.create(article=news1, tag=tag3)

    def test_news_titles(self):
        news1 = Article.objects.get(content='content1')
        news2 = Article.objects.get(content='content2')
        news3 = Article.objects.get(content='content3')
        self.assertEqual(Article.objects.count(), 3)
        self.assertEqual(news1.title, 'title1')
        self.assertEqual(news2.title, 'title2')
        self.assertEqual(news3.title, 'title3')

    def test_news_tags(self):
        news1 = Article.objects.get(content='content1')
        news3 = Article.objects.get(content='content3')
        news1_tags = news1.article_tags.all().select_related('tag').values_list('tag__name', flat=True)
        news3_tags = news3.article_tags.all().select_related('tag').values_list('tag__name', flat=True)
        self.assertIn('science', news1_tags)
        self.assertIn('mobile', news1_tags)
        self.assertIn('car', news3_tags)


class NewsListAPIViewsTests(APITestCase):
    def setUp(self):
        tag1 = Tag.objects.create(name='science')
        tag2 = Tag.objects.create(name='technology')
        tag3 = Tag.objects.create(name='mobile')
        tag4 = Tag.objects.create(name='car')

        news1 = Article.objects.create(title='title1', content='content1', author='author1',
                                       pub_date=datetime.date(2020, 1, 1))

        news2 = Article.objects.create(title='title2', content='content2', author='author2')

        news3 = Article.objects.create(title='title3', content='content3', author='author3',
                                       pub_date=datetime.date(2020, 1, 1))

        ArticleTag.objects.create(article=news1, tag=tag1)
        ArticleTag.objects.create(article=news2, tag=tag2)
        ArticleTag.objects.create(article=news2, tag=tag3)
        ArticleTag.objects.create(article=news3, tag=tag4)
        ArticleTag.objects.create(article=news1, tag=tag2)
        ArticleTag.objects.create(article=news1, tag=tag3)

    def test_get_all_news(self):
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)

        news = Article.objects.all()
        serializer = ArticleSerializer(news, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_news_by_tags(self):
        url = '/news/'
        response = self.client.get(url, {'tags': [self.tag1.name]})
        self.assertEqual(response.status_code, 200)

#         news = set(News.objects.filter(tags__name__in=[self.tag1.name]))
#         serializer = NewsSerializer(news, many=True)
#         self.assertEqual(response.data, serializer.data)
#
#         response = self.client.get(url, {'tags': [self.tag2.name]})
#         self.assertEqual(response.status_code, 200)
#
#         news = set(News.objects.filter(tags__name__in=[self.tag2.name]))
#         serializer = NewsSerializer(news, many=True)
#         self.assertEqual(response.data, serializer.data)
#
#         response = self.client.get(url, {'tags': [self.tag1.name, self.tag3.name]})
#
#         news = set(News.objects.filter(tags__name__in=[self.tag1.name, self.tag3.name]))
#         serializer = NewsSerializer(news, many=True)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data, serializer.data)
