from django.conf.urls import include
from django.urls import re_path as url
from django.urls import path
from rest_framework import routers, viewsets
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('googlelogin',views.GoogleLogin.as_view(),name='googlelogin'),
    path('leaderboard',views.leaderboard,name='leaderboard'),
    path('checkanswer',views.Answer.as_view(),name='check_answers'),
    path('refresh',TokenRefreshView.as_view(),name='token_refresh'),
    path('question',views.getquestion.as_view(),name='question api'),
    path('facebooklogin',views.facebooklogin.as_view(),name='facebooklogin'),
    path('status',views.configstatus,name='quiz_status'),
    path('timeline',views.TimelineData.as_view(),name='timeline_api'),
]