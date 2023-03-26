from django.urls import include, path


urlpatterns = [
    path('main/', include('ALC_dialog.urls')),
]
