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

    def validate(self,data): 
        answer=data.get("answer",None)
        player=self.context.get("player")
        print(player)
        #player=data.get("player")
        active=config.quiz_active(config)
        day=config.objects.all()[0].current_day
        curr_question=player[0].current_question
        question=Question.objects.filter(day=day,question_no=curr_question)
        result=Question.check_ans(Question,answer,question)
        if result:
           player[0].new_score(player)
        return {
                "result":result
            }
        
    
class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token and provider.
    """
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)