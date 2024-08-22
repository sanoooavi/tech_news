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
        news1.tags.add(tag1, tag3, tag4)
        news2.tags.add(tag2)
        news3.tags.add(tag3)

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
        news1_tags = list(news1.tags.all().values_list('name', flat=True))
        news3_tags = list(news3.tags.all().values_list('name', flat=True))
        self.assertIn('science', news1_tags)
        self.assertNotIn('car', news3_tags)
        self.assertIn('mobile', news1_tags)


class NewsListAPIViewsTests(APITestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name='science')
        self.tag2 = Tag.objects.create(name='technology')
        self.tag3 = Tag.objects.create(name='mobile')
        self.tag4 = Tag.objects.create(name='car')

        news1 = Article.objects.create(title='title1', content='content1', author='author1',
                                       pub_date=datetime.date(2020, 1, 1))

        news2 = Article.objects.create(title='title2', content='content2', author='author2')

        news3 = Article.objects.create(title='title3', content='content3', author='author3',
                                       pub_date=datetime.date(2020, 1, 1))

        news1.tags.add(self.tag1, self.tag3, self.tag4)
        news2.tags.add(self.tag2)
        news3.tags.add(self.tag3)

    def test_get_all_news(self):
        """Test retrieving all articles without any filters."""
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 3)

    def test_get_news_by_single_tag(self):
        """Test retrieving articles filtered by a single tag."""
        response = self.client.get('/news/', {'tags': [self.tag1.name]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'title1')

    def test_get_news_by_multiple_tags(self):
        """Test retrieving articles filtered by multiple tags."""
        response = self.client.get('/news/', {'tags': [self.tag3.name, self.tag4.name]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'title1')

    def test_get_news_by_nonexistent_tag(self):
        """Test retrieving articles filtered by a non-existent tag."""
        response = self.client.get('/news/', {'tags': ['nonexistent']})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)

    def test_get_news_with_no_tags(self):
        """Test retrieving all articles when no tags are provided."""
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 3)

    def test_get_article_count(self):
        """Test retrieving the total number of articles."""
        response = self.client.get('/news/count/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['article_count'], 3)

    def test_get_articles_by_author(self):
        """Test retrieving articles by a specific author."""
        response = self.client.get('/news/author/', {'author': 'author1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'title1')

    def test_get_articles_by_nonexistent_author(self):
        """Test retrieving articles by a non-existent author."""
        response = self.client.get('/news/author/', {'author': 'nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)

    def test_get_articles_by_author_without_providing_author(self):
        """Test error response when no author name is provided."""
        response = self.client.get('/news/author/')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], "Author name not provided")
