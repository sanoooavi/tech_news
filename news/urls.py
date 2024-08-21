from django.urls import path

from .views import *

urlpatterns = [
    path('', ArticleListView.as_view()),
    path('count/', ArticleCountView.as_view()),
    path('author/', ArticlesByAuthorView.as_view()),
]
