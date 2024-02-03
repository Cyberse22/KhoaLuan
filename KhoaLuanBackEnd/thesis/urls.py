from django.urls import path, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('user', views.CustomUserViewSet, basename='user')
routers.register('thesis', views.ThesisViewSet, basename='thesis')
routers.register('council', views.DefenseCouncilViewSet, basename='council')
routers.register('score', views.ThesisScoreViewSet, basename='score')

urlpatterns = [
    path('', include(routers.urls))
]
