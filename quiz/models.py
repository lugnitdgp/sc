from django.db import models
from django.contrib.auth.models import User
import datetime
import pytz
from pytz import timezone
utc= pytz.utc
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
        answer=answer.replace(" ","")
        answers=string.split(",")
        for ans in answers:
            z=ans.replace(" ","")
            if answer==z:
                return True
        return False
    def get_next_question(self,day,qno):
        question=self.objects.filter(day=day,question_no=qno)
        return question
           
class UserScore(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)
    name=models.CharField(max_length=55,null=True)
    email = models.EmailField(max_length=70,blank=True)
    score=models.IntegerField(default=0)
    rank=models.IntegerField(null=True)
    today = models.IntegerField(default=1)
    current_question=models.IntegerField()
    last_modified=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "{}-{}-Day{}-Score-{}".format(self.rank, self.name,self.day, self.score)
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
        # initializing current active config:
        configs= config.objects.all()



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
        curr_question=player.current_question
        if curr_config.q_no == curr_question:
            player.current_question = 1
            player.today = curr_config.current_day +1
        else:
            player.current_question += 1
        player.save()


class config(models.Model):
    current_day=models.IntegerField()
    q_no=models.IntegerField()
    quiz_active=models.BooleanField(default=True)
    quiz_start=models.DateTimeField()
    quiz_endtime=models.DateTimeField()
    def __str__(self):
        return "Day-{}".format(self.current_day)
    def quiz_active(self):
        # initializing current active config:
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
        if not self.pk:
            players=UserScore.objects.all()
            for player in players:
                player.current_question=1
                player.save()
            super(config, self).save(force_insert, force_update, *args, **kwargs)
