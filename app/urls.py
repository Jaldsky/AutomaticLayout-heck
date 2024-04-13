from django.urls import path

from app.views import register


urlpatterns = [
    path('', register, name='register'),
    # path('compare/', ),
    # path('history/'),
]
