from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User_profile(models.Model):
    user=models.ForeignKey('auth.User',primary_key=True)
    phone_no=models.IntegerField()
    isPolice=models.IntegerField()
    age=models.IntegerField()
    gender=models.TextField(default="Male")
    def __str__(self):
		return self.user.username;

class Address(models.Model):
	user=models.ForeignKey('auth.User',primary_key=True)
	house_no=models.TextField()
	locality=models.TextField()
	city=models.TextField()
	state=models.TextField()
	pin_code=models.IntegerField()

	def __str__(self):
		return self.user.username;

class Police(models.Model):
	user=models.ForeignKey('auth.User',primary_key=True)
	salary=models.IntegerField()
	description=models.TextField()
	post=models.CharField(max_length=30)
	rank=models.IntegerField()
	def __str__(self):
		return self.user.username;

class Civilian(models.Model):
	user=models.ForeignKey('auth.User',primary_key=True)
	isCriminal=models.IntegerField()
	salary=models.IntegerField(default=0)
	job=models.TextField(default="None")












