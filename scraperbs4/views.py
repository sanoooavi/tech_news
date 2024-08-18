from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from news.models import Article, Tag, ArticleTag
from .spider import scrape_zoomit  # Assuming your scraper is in a separate file


def populate_database(request):
    scrape_zoomit(start_page=1, end_page=5)  # Adjust the page range as needed
    return HttpResponse("Database populated!")
