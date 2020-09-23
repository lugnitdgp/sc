from rest_framework import serializers
from quiz.models import UserScore,Question,config
from django.contrib.auth.models import User
import datetime
from pytz import timezone
import pytz

utc= pytz.utc
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
        #initializing 
        configs= self.objects.all()
    


        # arr = [[config]*(no of instances of each day)]* no of days
        arr=[]
        arr = [0 for i in range(10)]      #initialized 10 days with 0 instances of each
        cnt = 1
        for con in configs:
            curr_day = con.current_day
            arr[curr_day] += 1
            cnt = max(curr_day, cnt)
        list_of_configs = []
        new = []
        for i in range(1,cnt+1):
            for j in configs:
                curr_day = j.current_day
                if curr_day == i:
                    new.append(j)
            list_of_configs.append(new)
            new = []

        maxi = datetime.datetime.now().replace(tzinfo=utc)
        choice = None
        default_choice = configs[0]
        for i in list_of_configs:
            
            maxi = datetime.datetime.now().replace(tzinfo=utc)
            for j in i:
                default_choice = j
                quiz_endtime = j.quiz_endtime.replace(tzinfo=utc)
                
                if maxi < quiz_endtime:
                    choice = j
                    
                    maxi = quiz_endtime
            if choice is not None:
                break
        if choice is None:
            choice = default_choice
        curr_config=choice
        #end
        day=curr_config.current_day
        
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
