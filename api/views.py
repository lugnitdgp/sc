from django.shortcuts import render
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from django.http import JsonResponse
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, throttle_classes,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import LeaderboardSerializer,AnswerSerializer,SocialSerializer
from quiz.models import UserScore,config,Question
from requests.exceptions import HTTPError
from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
# Create your views here.



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leaderboard(request):
    players=UserScore.leaderboard(UserScore)
    serializer=LeaderboardSerializer(players,many=True)
    return Response(serializer.data)

class Answer(APIView):
    permission_classes=(IsAuthenticated,)
    
    def post(self,request):
        player=UserScore.objects.filter(user=request.user)[0]
        print(player.name)
        answer=request.data.get("answer",None)
        #player=self.context.get("player")
        print(player)
        #player=data.get("player")
        #active=config.quiz_active(config)
        day=config.objects.all()[0].current_day
        curr_question=player.current_question
        question=Question.objects.filter(day=day,question_no=curr_question)
        result=Question.check_ans(Question,answer,question)
        if result:
           player.new_score(player)
        response={
            'status_code':status.HTTP_200_OK,
            'result':result
        }
        return Response(response)
class GoogleLogin(APIView):
    def post(self, request):
        payload = {'access_token': request.data.get("token")}  # validate the token
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content)

        # create user if not exist
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            user = User()
            user.username = data['name']
            # provider random default password
            user.password = make_password(BaseUserManager().make_random_password())
            user.email = data['email']
            user.save()
            score = UserScore(user=user,name=user.email, current_question = 1)
            score.save()

        token = RefreshToken.for_user(user)  # generate token without username & password
        response = {}
        response['username'] = user.username
        response['access_token'] = str(token.access_token)
        response['refresh_token'] = str(token)
        return Response(response)

class questionview(APIView):
    permission_classes=(IsAuthenticated,)

