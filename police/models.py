
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
class User_profile(models.Model):
    user=models.ForeignKey('auth.User',primary_key=True)
    phone_no=models.CharField(max_length=12)
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

class Station(models.Model):
	city=models.CharField(default="New Delhi",max_length=100)
	state=models.CharField(max_length=100)
	locality=models.CharField(max_length=100)
	name=models.CharField(max_length=100)
	slug=models.SlugField(primary_key=True,blank=True)
	def __str__(self):
		return self.name;
	def save(self,*args,**kwargs):
		if not self.slug:
			self.slug=slugify(self.name)
		super(Station,self).save(*args,**kwargs)


class Police(models.Model):
	user=models.ForeignKey('auth.User',primary_key=True)
	salary=models.IntegerField()
	description=models.TextField()
	post=models.CharField(max_length=30,default="Inspector")
	rank=models.IntegerField(default=5)
	station=models.ForeignKey(Station)
	def __str__(self):
		return self.user.username

class Civilian(models.Model):
	user=models.ForeignKey('auth.User',primary_key=True)
	isCriminal=models.IntegerField()
	salary=models.IntegerField(default=0)
	job=models.TextField(default="None")
	def __str__(self):
		return self.user.username


class Review(models.Model):
	id=models.AutoField(primary_key=True)
	description=models.TextField()
	civilian=models.ForeignKey(Civilian)
	date_posted=models.DateTimeField()
	station=models.ForeignKey(Station)

class Criminal_Record(models.Model):
	user=models.ForeignKey('auth.User',primary_key=True)
	jail=models.IntegerField(default=0)
	description=models.TextField()
	section=models.TextField()
	fine=models.IntegerField(default=0)

class Complaint(models.Model):
	description=models.TextField()
	pub_date = models.DateTimeField('date published')
	is_completed=models.BooleanField(default=False)
	user=models.ForeignKey('auth.User')
	police=models.ForeignKey(Police)
	def __str__(self):
		return self.description