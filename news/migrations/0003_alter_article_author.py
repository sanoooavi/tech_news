# Generated by Django 5.1 on 2024-08-14 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_article_url_alter_articletag_article_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
