from django.shortcuts import render
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, throttle_classes,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import LeaderboardSerializer,AnswerSerializer,SocialSerializer,QuestionSerializer
from quiz.models import UserScore,config,Question
from requests.exceptions import HTTPError
from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
import time
import datetime
from datetime import datetime
import pytz    # $ pip install pytz
import tzlocal # $ pip install tzlocal
from urllib3 import urlopen
from google.auth.transport import requests
from google.oauth2 import id_token
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
import requests as r
import pytz
from django.db.models import Q
from pytz import timezone
from decouple import config as configure
utc= pytz.utc

def verifyGoogleToken(token):
    CLIENT_ID = configure('CLIENT_ID', cast=str)
    try:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        return {
            "email": idinfo['email'],
            "username": idinfo['email'],
            "first_name": idinfo['name'],
            "image": idinfo['picture'],
            "status": 200
        }
    except ValueError:
        return {"status": 404, "message": "Your Token has expired. Please login/register again!"}
    
@api_view(['GET'])
def leaderboard(request):
    players=UserScore.leaderboard(UserScore)
    serializer=LeaderboardSerializer(players,many=True)
    return Response(serializer.data)
    
class getquestion(APIView):
    # permission_classes=(IsAuthenticated,)

    def get(self,request):
        # player=UserScore.objects.filter(user=request.user)[0]
        player=UserScore.objects.get(id=1)
        active=config.quiz_active(config)
        local_timezone = tzlocal.get_localzone() # get pytz tzinfo
        utc_time = datetime.strptime("2011-01-21 02:37:21", "%Y-%m-%d %H:%M:%S")
        local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        curr_config = config.current_config(config)
        print(curr_config.quiz_start)
        print(curr_config.quiz_endtime)
        if active:
            day= curr_config.current_day
            curr_day=player.today
            curr_question=player.current_question
            if curr_day > curr_config.current_day:             
                response={
                  "quiz_finished": True
                }
                return Response(response)
            if curr_day<day:                             #IMP: this is done so that for users who haven't completed the last day's task completely
                player.today = day                       #The ptr on current question is shifted to 1 and the day is shifted to whatever the present day is.
                player.current_question = 1              #EDGE CASE: ERROR if there are only 1 question in a round. 
                curr_day =player.today
                curr_question=player.current_question
                player.save()
            question=Question.objects.filter(day=day,question_no=curr_question)[0]
            serializer=QuestionSerializer(question)
            return Response(serializer.data)
        else:
            response= {
                "error":"quiz has ended"
            }
            return Response(response)


@api_view(['GET'])
def configstatus(request):
    choice = config.current_config(config)
    if choice:
       response={
       "current_day":choice.current_day,
       "start_time":choice.quiz_start.replace(tzinfo=utc),
       "end_time":choice.quiz_endtime.replace(tzinfo=utc),
       "round_questions": choice.q_no    
       }
       return Response(response)
    response={
        "status":404,
        "message":"no configs found"
    }
    return Response(response)

class Answer(APIView):
    permission_classes=(IsAuthenticated,)
    
    def post(self,request):
        player=UserScore.objects.filter(user=request.user)[0]
        print(player.name)
        answer=request.data.get("answer",None)
        print(player)
        active=config.quiz_active(config)
        curr_config = config.current_config(config)        
        if active:
            day=curr_config.current_day
            curr_day =player.today
            curr_question=player.current_question
            if curr_day>day:
                response={
                  "quiz_finished": True
                }
                return Response(response)
            if curr_day<day:
                player.today = day
                player.current_question= 1
                curr_day =player.today
                curr_question=player.current_question
                player.save()
            question=Question.objects.filter(day=day,question_no=curr_question)
            result=Question.check_ans(Question,answer,question)
            quiz_ended=False
            if result:
               player.new_score(player)
               UserScore.lboardSave(UserScore)
               curr_day =player.today 
               if curr_day > curr_config.current_day:
                   quiz_ended=True
            response={
                    'status_code':status.HTTP_200_OK,
                    'result':result,
                    'quiz_finished':quiz_ended
                }
        else:
           response= {
                "error":"quiz has ended"
            }
        return Response(response)
    
class GoogleLogin(APIView):
    def post(self, request):
        res = verifyGoogleToken(request.data.get('token'))
        if res['status'] == 404:
            return Response({
                "status": 404,
                "message": "Token expired."
            })
        try:
            user = User.objects.get(email=res['email'])
        except User.DoesNotExist:
            user = User()
            user.username = res['email']
            # provider random default password
            user.password = make_password(BaseUserManager().make_random_password())
            user.email = res['email']
            user.save()
            score = UserScore(user=user,name=res['first_name'],imgurl = res['image'], email = user.email, current_question = 1, last_modified =datetime.datetime.now().replace(tzinfo=utc))
            score.save()
            z = UserScore.lboardSave(UserScore)

        token = RefreshToken.for_user(user)  # generate token without username & password
        response = {}
        response['username'] = user.username
        response['access_token'] = str(token.access_token)
        response['refresh_token'] = str(token)
        response['image'] = str(res['image'])
        #register on leaderboard
        

        #adding quiz_finished tag for users who have finished the level
        player=UserScore.objects.filter(user=user)[0]
        active=config.quiz_active(config)
        curr_config = config.current_config(config)        
        if active:
            day=curr_config.current_day
            curr_day =player.today
            curr_question=player.current_question
            if curr_day>day:
                response['quiz_finished']= True
            else:
                response['quiz_finished']= False 
        else:
            response['error'] = "No active quizes"
        #end 
        return Response(response)


class facebooklogin(APIView):
    
    def post(self,request):
        print(request.data)
        accesstoken=request.data.get('accesstoken')
        expiration_time=request.data.get('expiration_time')
        print(expiration_time)
        userID=request.data.get('userID')
        if(int(expiration_time) < int(time.time())):
            content= {"status": 404}
            return Response(content)
        else:
            url = "https://graph.facebook.com/{}".format(userID)
            parameters = {
                'fields': 'name,email,picture',
                'access_token': accesstoken
            }
            idInfo = r.get(url=url, params=parameters).json()

            email= idInfo['email']
            name= idInfo['name']
            email = email
            name = name

            image= idInfo['picture']['data']['url']
            try:
                user = User.objects.get(email=email)
                player=UserScore.objects.filter(user=user)[0]                           #FB profile pic at higher priority than google.
                player.imgurl = image                                                   #However this generates an issue: Anyone who swtiches to fb from google
                player.save()                                                           #have his last modified time, changed to now(). So he might lose a couple   
            except User.DoesNotExist:                                                   #places on the leaderboard. Solution: Make a custom save option/ Change auto_now= false
                user = User()
                user.username = email
                user.email = email
                # provider random default password
                user.password = make_password(BaseUserManager().make_random_password())
                user.save()
                score = UserScore(user=user,name=name,imgurl= image, email = user.email, current_question = 1, last_modified =datetime.datetime.now().replace(tzinfo=utc))
                score.save()
                z = UserScore.lboardSave(UserScore)

        token = RefreshToken.for_user(user)  # generate token without username & password
        response = {}
        response['username'] = user.username
        response['access_token'] = str(token.access_token)
        response['refresh_token'] = str(token)
        response['image']= image[0]
        
        #adding quiz_finished tag for users who have finished the level
        player=UserScore.objects.filter(user=user)[0]
        active=config.quiz_active(config)
        curr_config = config.current_config(config)        
        if active:
            day=curr_config.current_day
            curr_day =player.today
            curr_question=player.current_question
            if curr_day>day:
                response['quiz_finished']= True
            else:
                response['quiz_finished']= False 
        else:
            response['error'] = "No active quizes"
        #end 
        return Response(response)
        
    
class TimelineData(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self,request):
        player=UserScore.objects.filter(user=request.user)[0]
        active=config.quiz_active(config)
        curr_config = config.current_config(config)
        current_time=datetime.datetime.now().replace(tzinfo=utc)
        if current_time < curr_config.quiz_start.replace(tzinfo=utc):
            response = {
                "quiz_started":False
            }
            return Response(response)
        if active:
            day= curr_config.current_day
            curr_day=player.today
            curr_question=player.current_question
            if curr_day > curr_config.current_day:             
                response={
                  "quiz_finished": True
                }
                return Response(response)
            if curr_day<day:                             #IMP: this is done so that for users who haven't completed the last day's task completely
                player.today = day                       #The ptr on current question is shifted to 1 and the day is shifted to whatever the present day is.
                player.current_question = 1              #EDGE CASE: ERROR if there are only 1 question in a round. 
                curr_day =player.today
                curr_question=player.current_question
                player.save()
            
            ##question=Question.objects.filter(day=day,question_no=curr_question)[0]
            #serializer=QuestionSerializer(question)
            response={
                'current_question':curr_question
            }
            return Response(response)
        else:
            response= {
                "error":"quiz has ended"
            }
            return Response(response)
