from rest_framework import serializers
from quiz.models import UserScore,Question,config
from django.contrib.auth.models import User

class LeaderboardSerializer(serializers.ModelSerializer):

    class Meta:
        model=UserScore
        fields=['user','name','score','rank']

class QuestionSerializer(serializers.ModelSerializer):


      class Meta:
          model=Question
          fields=['question','id','question_no','audio','image','hint']

class AnswerSerializer(serializers.Serializer):

    answer=serializers.CharField(max_length=255)

    def validate(self,data,player): 
        answer=data.get("answer",None)
        day=config.objects.all().current_day
        curr_question=player.current_question


