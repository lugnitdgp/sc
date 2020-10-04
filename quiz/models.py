from django.db import models
from django.contrib.auth.models import User
import datetime
import pytz
from pytz import timezone
from django.core.cache import cache
utc= pytz.utc
# Create your models here.



class Question(models.Model):
    question=models.CharField(max_length=550)
    day=models.IntegerField()
    question_no=models.IntegerField()
    answer=models.CharField(max_length=100)
    audio=models.FileField(upload_to='media/audios',blank=True)
    image=models.ImageField(upload_to='media/images',blank=True)
    hint=models.CharField(max_length=555,default='N/A')
    def __str__(self):
        return "Day-{}-Q-{} : {}".format(self.day, self.question_no, self.question)

    class Meta:
        ordering=['day','question_no']

    def check_ans(self,answer,question):
        string = question[0].answer.lower()                         #the actual answer is stored here
        answer = answer.lower()                                     #answer given by player is stored here
        answer=answer.replace(" ","")                               #spaces removed from user given answer
        answers=string.split(",")                                   #answers now contains all the probable answers(yes, more than one answers are possible)
        for ans in answers:
            z=ans.replace(" ","")                                   #each ans's spaces removed and compared against user's given answer
            if answer==z:       
                return True                                         #if atleast one of them matches, it gives correct ans; else false
        return False
    def get_next_question(self,day,qno):
        question=self.objects.filter(day=day,question_no=qno)
        return question
           
class UserScore(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)
    name=models.CharField(max_length=55,null=True)
    imgurl = models.CharField(max_length=500, null=True)
    email = models.EmailField(max_length=70,blank=True)
    score=models.IntegerField(default=0)
    rank=models.IntegerField(null=True)
    today = models.IntegerField(default=1)
    current_question=models.IntegerField()
    last_modified=models.DateTimeField(auto_now=False)
    
    def __str__(self):
        return "{}-{}-Day{}-Score-{}".format(self.rank, self.name,self.today, self.score)
    class Meta:
        ordering =['-score','last_modified']

    def leaderboard(self):
        val = cache.get('lboard')                                   #Checking if leaderboard cache exists.
        if val is not None:                                         #Then it would be returned else, the whole function runs
            print('data fetched from cache')
            return val
        players=self.objects.all()
        rank=1
        for player in players:                                      #rank is decided by meta, score then last correct submission
            player.rank=rank
            rank +=1
            player.save()                                           #This line makes all last modified to -> way the leaderboard is made. 
        cache.set('lboard', players, 10800) 
        return players                                              #Definitely not recommended. Solu: make custom save function/ date time field must be changed to auto_now = False

    def new_score(self,player):
        
        player.score+=10                                            # 10 added
        curr_config = config.current_config(config)
        curr_question=player.current_question
        if curr_config.q_no == curr_question:
            player.current_question = 1                             #if the max no. of questions are reached for the day, then ptr is moved
            player.today = curr_config.current_day +1               #to the next day, questions ptr is shifted to
        else:
            player.current_question += 1                            #else the questions ptr is shifted forward by one 
        player.last_modified =datetime.datetime.now().replace(tzinfo=utc)
        player.save()

    def lboardSave(self):
        players=self.objects.all()
        rank=1
        for x in players:                                      #rank is decided by meta, score then last correct submission
            x.rank=rank
            rank +=1
            x.save()
        cache.set('lboard', players, 10800)                            #Leaderboard Cache populated. The cache is updated everytime there is a change in score of a user


class config(models.Model):
    current_day=models.IntegerField()
    q_no=models.IntegerField()
    quiz_active=models.BooleanField(default=True)
    quiz_start=models.DateTimeField()
    quiz_endtime=models.DateTimeField()
    class Meta:
        ordering =['-current_day','quiz_endtime']
    def __str__(self):
        active = config.current_config(config)
        s= ""
        z= ""
        if self.quiz_endtime.replace(tzinfo=utc)< datetime.datetime.now().replace(tzinfo=utc):
            z = "-expired"
        if self== active:
            s = "-ONLINE"
            if z=="-expired":
                s="-Current Config"
        return "Day-{} {}{}".format(self.current_day,s,z)

    def current_config(self):

        configs= self.objects.all()
                                                                    # arr = [[config]*(no of instances of each day)]* no of days
        arr=[]
        arr = [0 for i in range(10)]                                #initialized 10 days with 0 instances of each
        cnt = 1
        for con in configs:
            curr_day = con.current_day
            arr[curr_day] += 1  
            cnt = max(curr_day, cnt)       
        list_of_configs = []        
        new = []
        for i in range(1,cnt+1):                                    #This is like a vector of vectors with ith day config in list[i] vector. So we basically choose 1 out of each day,
            for j in configs:
                curr_day = j.current_day
                if curr_day == i:
                    new.append(j)
            list_of_configs.append(new)
            new = []                

        maxi = datetime.datetime.now().replace(tzinfo=utc)
        choice = None
        if len(configs) == 0: 
            default_choice = None
        else: 
            default_choice = configs[0]
        for i in list_of_configs:
            
            maxi = datetime.datetime.now().replace(tzinfo=utc)
            for j in i:
                default_choice = j
                quiz_endtime = j.quiz_endtime.replace(tzinfo=utc)
                
                if maxi < quiz_endtime:                             #the config with the maximum endtime is chosen incase of a clash
                    choice = j
                    
                    maxi = quiz_endtime
            if choice is not None:                                  #IMP: if there is a valid config with a lower day it would be given higher priority
                break
        if choice is None:                                          #if there are no configs, the case is handled in quiz_active () function
            choice = default_choice
        curr_config=choice                  
        
        return curr_config

    def quiz_active(self):
        curr_config = self.current_config(self)                     #current valid config is found
        if curr_config is None:
            return False                                            
        current_time=datetime.datetime.now().replace(tzinfo=utc)    #No config in the DB     
        quiz_endtime=curr_config.quiz_endtime.replace(tzinfo=utc)
        print(curr_config.quiz_endtime)
        print(current_time)  
        if current_time>quiz_endtime:                               #if the valid config's time endtime is yet to come, then its an active quiz. The starttime value is 
            curr_config.quiz_active=False                           #compared in the frontend. 
            print(current_time>quiz_endtime)
            return False
        return True

