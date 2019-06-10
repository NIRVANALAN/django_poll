from django.db import models
import datetime
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    question_txt = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    # add descriptions in Question.objects.all()
    def __str__(self):
        return self.question_txt
    
    def was_published_recently(self):
        '''
        for show
        '''
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete = models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text