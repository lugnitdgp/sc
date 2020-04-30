from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Question(models.Model):
    question=models.CharField(max_length=550)
    day=models.IntegerField()
    answer=models.CharField(max_length=100)
    audiofield=models.FileField(upload_to='media',blank=True)
    image=models.ImageField(upload_to='media/images',blank=True)
    def __str__(self):
        return "{}-Day{}".format(self.question,self.day)

    class Meta:
        ordering=['day']

class Answer(models.Model):
    question=models.ForeignKey(to=Question,on_delete=models.CASCADE,related_name='qa')
    answer=models.CharField(max_length=100)
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)

class UserScore(models.Model):
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)
    score=models.IntegerField(default=0)
    last_modified=models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering =['score']

    