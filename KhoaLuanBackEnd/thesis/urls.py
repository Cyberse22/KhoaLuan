from django.urls import path, include
from . import views
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('users', views.CustomUserViewSet, basename='users')
routers.register('thesis', views.ThesisViewSet, basename='thesis')
routers.register('councils', views.DefenseCouncilViewSet, basename='councils')
routers.register('scores', views.ThesisScoreViewSet, basename='scores')

urlpatterns = [
    path('', include(routers.urls))
]
