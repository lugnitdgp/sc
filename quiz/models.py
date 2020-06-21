from django.db import models
from django.contrib.auth.models import User
import datetime
import pytz

utc=pytz.UTC
# Create your models here.
class Question(models.Model):
    question=models.CharField(max_length=550)
    day=models.IntegerField()
    question_no=models.IntegerField()
    answer=models.CharField(max_length=100)
    audio=models.FileField(upload_to='media/audios',blank=True)
    image=models.ImageField(upload_to='media/images',blank=True)
    hint=models.CharField(max_length=555,default='na')
    def __str__(self):
        return "{}-Day{}".format(self.question,self.day)

    class Meta:
        ordering=['day','question_no']

    def check_ans(self,answer,question):
        string = question[0].answer.lower()
        answer = answer.lower()
        answers=string.split(",")
        for ans in answers:
            if answer==ans:
                return True
        return False
    def get_next_question(self,day,qno):
        question=self.objects.filter(day=day,question_no=qno)
        return question
           
class UserScore(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)
    name=models.CharField(max_length=55,null=True)
    score=models.IntegerField(default=0)
    rank=models.IntegerField(null=True)
    current_question=models.IntegerField()
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
        player.current_question +=1
        player.save()


class config(models.Model):
    current_day=models.IntegerField()
    q_no=models.IntegerField()
    quiz_active=models.BooleanField(default=True)
    quiz_start=models.DateTimeField()
    quiz_endtime=models.DateTimeField()

    def quiz_active(self):
        curr_config=self.objects.all()[0]
        current_time=datetime.datetime.now().replace(tzinfo=utc)  
        quiz_endtime=curr_config.quiz_endtime.replace(tzinfo=utc)
        print(curr_config.quiz_endtime)
        print(current_time)  
        if current_time>quiz_endtime:
            curr_config.quiz_active=False
            print(current_time>quiz_endtime)
            return False
        return True
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        players=UserScore.objects.all()
        for player in players:
            player.current_question=1
            player.save()
        super(config, self).save(force_insert, force_update, *args, **kwargs)
