from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers, viewsets
from . import views


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('googlelogin',views.GoogleLogin.as_view(),name='googlelogin'),
    path('leaderboard',views.leaderboard,name='leaderboard'),
    path('checkanswer',views.Answer.as_view(),name='check_answers'),
]