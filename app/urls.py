from django.urls import path
from .views import execute

urlpatterns = [
    path('', execute, name='app'),
]
