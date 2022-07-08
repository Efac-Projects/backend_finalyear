from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('check', views.checkStatues),
    path('url', views.sendUrl),
    path('model', views.checkHostedMOdel)
]

