from django.urls import path
from .views import populate_database

urlpatterns = [
    path('', populate_database)
]
