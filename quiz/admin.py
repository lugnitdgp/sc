from django.contrib import admin
from .models import Question,UserScore,config

admin.site.register(Question)
admin.site.register(UserScore)
admin.site.register(config)
# Register your models here.
