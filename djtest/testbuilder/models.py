from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Question(models.Model):
	question = models.CharField(primary_key=True, max_length=200)
	quiz = models.ForeignKey("Quiz", related_name="quiz", on_delete=models.CASCADE)

class Choice(models.Model):
	question = models.ForeignKey("Question", related_name="choices", on_delete=models.CASCADE)
	choice = models.CharField("Choice", max_length=50)
	isCorrect = models.BooleanField("Choice", default=False)
	
class ShortAnswer(models.Model):
	question= models.ForeignKey("Question", related_name="shortanswer", on_delete=models.CASCADE)
	answer = models.CharField(max_length=100)

class Quiz(models.Model):
	title = models.CharField(max_length=100)
	question_count = models.IntegerField(default=0)
	passcode = models.CharField(primary_key=True, max_length=50)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class Profiles(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	occupation = models.IntegerField()
	#teacher = models.BooleanField(choices=OCCUPATION)
	#teacher = models.BooleanField(default=False)