from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Question(models.Model):
    question=models.CharField(max_length=550)
    day=models.IntegerField()
    question_no=models.IntegerField()
    answer=models.CharField(max_length=100)
    audiofield=models.FileField(upload_to='media',blank=True)
    image=models.ImageField(upload_to='media/images',blank=True)
    hint=models.CharField(max_length=555,default='na')
    def __str__(self):
        return "{}-Day{}".format(self.question,self.day)

    class Meta:
        ordering=['day','question_no']

    def check_ans(self,answer,question):
        if question.answer==answer:
            return True

           
class UserScore(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)
    name=models.CharField(max_length=55,null=True)
    score=models.IntegerField(default=0)
    rank=models.IntegerField(null=True)
    last_modified=models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering =['-score','last_modified']

    def leaderboard(self):
        players=self.objects.all()
        rank=1
        for player in players:
            player.rank=rank
            rank +=1
        return players

    def new_score(self,player):
        player.score+=10
        player.save()


class config(models.Model):
    current_day=models.IntegerField()
    q_no=models.IntegerField()
    quiz_active=models.BooleanField()
    quiz_start=models.DateTimeField()
    quiz_endtime=models.DateTimeField()

    def quiz_active(self):
        current_time=datetime.datetime()
        if current_time==self.quiz_endtime:
            self.quiz_active=False
