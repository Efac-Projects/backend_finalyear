from django.urls import path, include
from django.views import View
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('url', views.sendUrl),
    path('model', views.checkHostedMOdel),
    path('levelprediction', views.level_prediction),
    path('reinforcement', views.sendOptimizeSchedule)
]
