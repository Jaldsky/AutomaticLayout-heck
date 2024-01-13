from django.urls import path
from app.views import execute

urlpatterns = [
    path('', execute, name='app'),  # service location in the root
]
