
from django.urls import path, include
from . import views
from rest_framework import routers

urlpatterns = [
    path('checkpolly', views.checkPolly),
    path('checkspeech', views.getSpeechOutput)
]
