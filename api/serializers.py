from rest_framework import serializers
from quiz.models import UserScore
from django.contrib.auth.models import User




class LeaderboardSerializer(serializers.ModelSerializer):

    class Meta:
        model=UserScore
        fields=['user','name','score','rank']

        
