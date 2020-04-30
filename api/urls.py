from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers, viewsets
from . import views


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]