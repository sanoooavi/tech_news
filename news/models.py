from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=200, null=True)
    url = models.URLField(max_length=200, null=True)
    pub_date = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='articles')

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
