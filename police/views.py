from django.shortcuts import render,redirect,get_object_or_404,render_to_response
from django.contrib.auth.models import User
from django.db import IntegrityError,connection
from django.http import HttpResponse,Http404
from django.contrib.auth import authenticate,login,logout
from .models import User_profile,Police,Address,Civilian,Criminal_Record,Station,Review,Complaint
from .forms import User_profile_form,Police_form,Address_form,Civilian_form,Criminal_Record_form
from django.contrib import messages
from django.contrib.messages import get_messages
from django.utils import timezone
from django.template import RequestContext
import json

def index(request):
	return render(request,'police/index.html')

def signuppage(request):
	if request.user.is_authenticated():
		return redirect('/fill_details')

	if request.method == 'POST':
		try:
			username=password=lastname=firstname=''	
			email     = request.POST.get('email')
			firstname = request.POST.get('firstname')
			lastname  = request.POST.get('lastname')
			username  = request.POST.get('username')
			password  = request.POST.get('password')
			user=User.objects.create_user(username,email,password)
			user.first_name=firstname
			user.last_name=lastname
			user.save()
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request,user)
			status='done'
		except IntegrityError:
			status = 'user already exists'
			return render(request,'police/signup.html',{'status':status})
		else:
			messages.info(request,'Welcome! Successfully signed up.')
			status = 'new user was created'
		return redirect('/fill_details')
	else:
		return render(request,'police/signup.html')

def signup_detail(request):
	if request.user.is_authenticated():
		if User_profile.objects.filter(user=request.user).exists():
			if User_profile.objects.get(user=request.user).isPolice==1:
				return redirect('/police/'+request.user.username)
			else:
				return redirect('/civilian/'+request.user.username)
		if request.method == 'POST':
			if request.POST.get('police')=="police":
				form=User_profile_form(request.POST)
				print form
				if form.is_valid():
					print 'Form is valid BC'
					temp=form.save(commit=False)
					temp.user=request.user
					temp.gender=request.POST.get('gender')
					temp.isPolice=1
					temp.save()
					return redirect('/police/'+request.user.username)
				else:
					error="fill in the details properly"
					return redirect('/fill_details',{'error':error})
			else:
				form=User_profile_form(request.POST)
				if form.is_valid():
					temp=form.save(commit=False)
					temp.user=request.user
					temp.isPolice=0
					temp.gender=request.POST.get('gender')
					temp.save()
					return redirect('/civilian/'+request.user.username)
				else:
					error="fill in the details properly"
					return redirect('/fill_details',{'error':error})
		else:
			form=User_profile_form()
			return render(request,'police/signup_detail.html',{'form':form})
	else:
		return redirect('/login')

def welcomepolice(request,username):
	if not request.user.is_authenticated():
		messages.error(request, 'you need to login '+username)
		return redirect('/login')
	if username != request.user.username:
		logout(request)
		messages.error(request, 'login with username '+username)
		return redirect('/login')
	if User_profile.objects.get(user=request.user).isPolice==0:
		logout(request)
		messages.error(request, 'you are a civilian and you cannot view a policeman\'s account')
		return redirect('/login')
	if request.method=='POST' and request.POST.get('civilian')=="civilian":
		get_user_name=request.POST.get('username')
		requested_user=User.objects.filter(username=get_user_name)
		if requested_user.exists():
			query=User_profile.objects.filter(user=requested_user[0])
			if query.exists() and query[0].isPolice==0:
				return redirect('/detail/civilian/'+get_user_name)
		messages.error(request, 'no user with the '+get_user_name+' was found')
		return redirect('/police/'+username)

	if request.method=='POST' and request.POST.get('police')=="police":
		get_user_name=request.POST.get('username')
		requested_user=User.objects.filter(username=get_user_name)
		if requested_user.exists():
			query=User_profile.objects.filter(user=requested_user[0])
			if query.exists() and query[0].isPolice==1:
				policeman=Police.objects.filter(user=requested_user[0])
				if not policeman.exists():
					messages.error(request,'the user\'s details are not yet filled up')
					return redirect('/police/'+username)
				curr_police=Police.objects.filter(user=request.user)
				if curr_police.exists():
					# if policeman[0].rank >= curr_police[0].rank:
						# return redirect('/detail/police/'+get_user_name)
					# else:
					# 	messages.error(request,'you cannot view your senior\'s account')
					# 	return redirect('/police/'+username)
					if policeman[0].rank < curr_police[0].rank:
						messages.error(request,'Your can see only basic details for your seniors.')
					return redirect('/detail/police/'+get_user_name)
				else:
					messages.error(request,'fill up your details first')
					return redirect('/police/'+username)
		messages.error(request, 'no police with the username '+get_user_name+' was found')
		return redirect('/police/'+username)
	else:
		curr_user=User_profile.objects.get(user=request.user)
		return render(request,'police/welcome_police.html',{'user':request.user,'curr_user':curr_user})

def editpolice(request,username):
	if not request.user.is_authenticated():
		messages.error(request, 'you need to login '+username)
		return redirect('/login')
	if username != request.user.username:
		logout(request)
		messages.error(request, 'login with username '+username)
		return redirect('/login')
	if User_profile.objects.get(user=request.user).isPolice==0:
		logout(request)
		messages.error(request, 'you are a civilian and you cannot edit a policeman\'s account')
		return redirect('/login')
	policeStations=Station.objects.all()
	print policeStations
	if request.method == 'POST':
		form1=Police_form(request.POST)
		form2=Address_form(request.POST)
		if form1.is_valid() and form2.is_valid():
			post1=form1.save(commit=False)
			post1.user=request.user
			temp=request.POST.get('post_police')
			post1.post=temp

			rank=0
			if temp=="Commissioner":
				rank=1
			elif temp=="Joint Commissioner":
				rank=2
			elif temp=="Deputy Commissioner":
				rank=3
			elif temp=="Assistant Superintendent":
				rank=4
			elif temp=="Inspector":
				rank=5
			elif temp=="Assistant Inspector":
				rank=6
			elif temp=="Sub-Inspector":
				rank=7
			else:
				rank=8

			post1.rank=rank
			post1.station_id=request.POST.get('station_police')
			post1.save()
			post2=form2.save(commit=False)
			post2.user=request.user
			post2.save()
			messages.info(request, "changes have been saved sucessfully")
			return redirect('/police/'+request.user.username)
		else:
			error='fill in the details properly'
			return render(request,'police/editpolice.html',{'error':error,'stations':policeStations})
	else:
		if Police.objects.filter(user=request.user).exists() and Address.objects.filter(user=request.user).exists():
			address=Address.objects.get(user=request.user)
			details=Police.objects.get(user=request.user)
			post=details.post
			return render(request,'police/editpolice.html',{'post':post,'stations':policeStations,'details':details,'address':address,'user':request.user})
		else:
			form1=Police_form()
			form2=Address_form()
			return render(request,'police/editpolice.html',{'user':request.user,'stations':policeStations})


def editcivilian(request,username):
	isCriminal=0
	if not request.user.is_authenticated():
		messages.error(request, 'you need to login '+username)
		return redirect('/login')
	if username != request.user.username:
		logout(request)
		messages.error(request, 'login with username '+username)
		return redirect('/login')
	if User_profile.objects.get(user=request.user).isPolice==1:
		logout(request)
		messages.error(request, 'you are a police and you cannot edit a civilian\'s account')
		return redirect('/login')
	if request.method == 'POST':
		form1=Civilian_form(request.POST)
		form2=Address_form(request.POST)
		if form1.is_valid() and form2.is_valid():
			post1=form1.save(commit=False)
			post1.user=request.user
			post1.isCriminal=isCriminal
			post1.save()
			post2=form2.save(commit=False)
			post2.user=request.user
			post2.save()
			messages.error(request, "changes have been saved sucessfully")
			return redirect('/civilian/'+request.user.username)
		else:
			error='fill in the details properly'
			return render('police/editcivilian.html',{'error':error})
	else:
		if Civilian.objects.filter(user=request.user).exists() and Address.objects.filter(user=request.user).exists():
			address=Address.objects.get(user=request.user)
			details=Civilian.objects.get(user=request.user)
			isCriminal=Civilian.objects.get(user=request.user).isCriminal
			return render(request,'police/editcivilian.html',{'isCriminal':isCriminal,'details':details,'address':address})
		else:
			form1=Civilian_form()
			form2=Address_form()
			return render(request,'police/editcivilian.html',{'isCriminal':isCriminal,'user':request.user})

def welcomecivilian(request,username):
	if not request.user.is_authenticated():
		messages.error(request, 'you need to login '+username)
		return redirect('/login')
	if username != request.user.username:
		logout(request)
		messages.error(request, 'login with username '+username)
		return redirect('/login')
	if User_profile.objects.get(user=request.user).isPolice==1:
		logout(request)
		messages.error(request, 'you are a policeman and you cannot view a civilian\'s details')
		return redirect('/login')
	curr_user=User_profile.objects.get(user=request.user)
	return render(request,'police/welcome_civilian.html',{'user':request.user,'curr_user':curr_user})

def loginpage(request):
	# error="wrong credientials entered"
	# if request.user.is_authenticated():
	# 	return redirect('/fill_details')
	# username=password=''
	# if request.method == 'POST':
	# 	username = request.POST.get('username')
	# 	password = request.POST.get('password')
	# 	user = authenticate(username=username, password=password)
	# 	if user is not None and user.is_active:
	# 		login(request,user)
	# 		return redirect('/fill_details')
	# 	else:
	# 		return render(request,'police/login.html',{'error':error})
	# else:
	# 	return render(request,'police/login.html')
	# 	
	errors=[]
	if request.user.is_authenticated():
		return redirect('/fill_details')
	username=password=''
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None and user.is_active:
			login(request,user)
			return redirect('/fill_details')
		else:
			errors.append('Wrong credentials entered')
	return render(request,'police/login.html',{'errors':errors})

def logout_user(request):
	if request.user.is_authenticated():
		logout(request)
	return redirect('/login')

def civiliandatabase(request):
	if not request.user.is_authenticated():
		messages.error(request, 'you need to login first with a valid policeman account')
		return redirect('/login')
	if User_profile.objects.get(user=request.user).isPolice==0:
		logout(request)
		messages.error(request, 'you are a civilian and the information you requested is highly confidential which is only available to the police')
		return redirect('/login')
	else:
		civilianlist=User_profile.objects.filter(isPolice=0).order_by('age')
		return render(request,'police/civilianlist.html',{'result':civilianlist})

def criminaldatabase(request):
	if not request.user.is_authenticated():
		messages.error(request, 'you need to login first with a valid policeman account')
		return redirect('/login')
	if User_profile.objects.get(user=request.user).isPolice==0:
		logout(request)
		messages.error(request, 'you are a civilian and the information you requested is highly confidential which is only available to the police')
		return redirect('/login')
	else:
		criminallist=Civilian.objects.filter(isCriminal=1)
		return render(request,'police/criminallist.html',{'result':criminallist})

def civiliandetail(request,username):
	if not request.user.is_authenticated():
		messages.error(request, 'you need to login first with a valid policeman account')
		return redirect('/login')

	try:
		user=User_profile.objects.get(user=request.user)
	except User_profile.DoesNotExist:
		logout(request)
		messages.error(request, 'Please enter your details')
		return redirect('/fill_details')
	if user.isPolice==0:
		logout(request)
		messages.error(request,'You are a civilian and the information you requested is highly confidential which is only available to the police')
		return redirect('/login')
	# if User_profile.objects.get(user=request.user).isPolice==0:
	# 	logout(request)
	# 	messages.error(request, 'you are a civilian and the information you requested is highly confidential which is only available to the police')
	# 	return redirect('/login')

	if request.method=='POST':
		form=Criminal_Record_form(request.POST)
		if form.is_valid:
			criminalrecord=form.save(commit=False)
			requested_user=User.objects.get(username=username)
			criminalrecord.user=requested_user
			criminalrecord.save()
			civilian=Civilian.objects.filter(user=requested_user)
			if civilian.exists():
				civilian=Civilian.objects.get(user=requested_user)
				civilian.isCriminal=1
				civilian.save()
			else:
				temp=Civilian(user=requested_user,isCriminal=1,salary=0,job="none")
				temp.save()
			messages.success(request,'successfully accused of crime')
			return redirect('/police/'+request.user.username)
		else:
			messages.error(request,'could not save your details... please try again')
			return redirect('/police/'+request.user.username)
	else:
		requested_user=User.objects.filter(username=username)
		userprofile=User_profile.objects.get(user=requested_user[0])
		query1=Civilian.objects.filter(user=requested_user[0])

		if requested_user.exists() and query1.exists() and userprofile.isPolice==0:
			address=Address.objects.get(user=requested_user[0])
			criminal=Criminal_Record.objects.filter(user=requested_user[0])
			form=Criminal_Record_form()
			return render(request,'police/civiliandetail.html',{'criminal':criminal,'civilian':query1[0],'address':address,'userprofile':userprofile,'req_user':requested_user[0]})
		else:
			messages.error(request, 'no such user found')
			return redirect('/police/'+request.user.username)

def policedetail(request,username):
	# get_user_name=username
	# requested_user=User.objects.filter(username=get_user_name)
	# if requested_user.exists():
	# 	query=User_profile.objects.filter(user=requested_user[0])
	# 	if query.exists() and query[0].isPolice==1:
	# 		police=Police.objects.filter(user=requested_user[0])
	# 		if not police.exists():
	# 			messages.error(request,'The user\'s details are not yet filled up')
	# 			return redirect('/police/'+request.user.username)
	# 		curr_police=Police.objects.filter(user=request.user)
	# 		if curr_police.exists():
	# 			if police[0].rank >= curr_police[0].rank:
	# 				user=User.objects.filter(username=username)
	# 				address=Address.objects.filter(user=user)
	# 				return render(request,'police/policedetail.html',{'user':user[0],'address':address[0],'userprofile':query[0],'police':police[0]})
	# 			else:
	# 				messages.error(request,'you cannot view your senior\'s account')
	# 				return redirect('/police/'+request.user.username)
	# 		else:
	# 			messages.error(request,'fill up your details first')
	# 			return redirect('/police/'+request.user.username)
	# messages.error(request, 'no police with the username '+get_user_name+' was found')
	# return redirect('/police/'+request.user.username)
	requested_user=User.objects.filter(username=username)
	if requested_user.exists():
		userInfo=User_profile.objects.filter(user=requested_user[0])
		if userInfo.exists() and userInfo[0].isPolice==1:
			police=Police.objects.filter(user=requested_user[0])
			if not police.exists():	
				return render(request,'police/policedetail.html',{'detailsFilled':False})
			deferred=True
			if request.user.is_authenticated():
				curr_police=Police.objects.filter(user=request.user)
				if curr_police.exists() and police[0].rank>=curr_police[0].rank:
					deferred=False
			address=Address.objects.filter(user=requested_user)
			complaints=Complaint.objects.filter(police=police[0])
			print complaints
			return render(request,'police/policedetail.html',{'detailsFilled':True,'complaints':complaints,'details':{'req_user':requested_user[0],'address':address[0],'userprofile':userInfo[0],'police':police[0]},'deferred':deferred})
	raise Http404('No such record in our database')


#POLICE STAION VIEW
def policestation(request,slug):
	if request.method=='GET':
		station_slug=slug
		station=get_object_or_404(Station,slug=station_slug)
		police_wale=Police.objects.filter(station=station)
		reviews=Review.objects.filter(station=station)
		return render(request,'police/station/station.html',{'police_wale':police_wale,'station':station,'reviews':reviews})

def addReview(request,slug):
	if request.method=='POST':
		station=Station.objects.get(slug=slug)
		if(request.user.is_authenticated()):
			try:
				user=User_profile.objects.get(user=request.user)
			except User_profile.DoesNotExist:
				return HttpResponse(json.dumps({'message':'Please <a href="/fill_details">fill your details</a> first.','success':False}))
			if user.isPolice==1:
				return HttpResponse(json.dumps({'message':'Police can review a police station.'}))
			try:
				civilian=Civilian.find()
			except: 
				return HttpResponse(json.dumps({'message':'Sir, please enter your details for <a href="/civilian/'+request.user.username+'/edit">verification</a>'}))
			x=Review(station=station,civilian=civilian,description=request.POST.get('description'),date_posted=timezone.now())
			x.save()
			print x
			return HttpResponse(json.dumps({'message':'Successfully posted the review.','review':{'description':x.description,'user':request.user.username},'success':True}));
		else:
			return HttpResponse(json.dumps({'message':'You must be logged in to submit the review.','success':False}));


def addComplaint(request,police_username):
	if request.method=='POST':
		req_user=User.objects.get(username=police_username)
		if(request.user.is_authenticated()):
			try:
				police=Police.objects.get(user=req_user)
			except Police.DoesNotExist:
				return HttpResponse(json.dumps({'message':'No such policeman. Blah.','success':False}));
			x=Complaint(police=police,user=request.user,description=request.POST.get('complaint'),pub_date=timezone.now(),is_completed=False)
			x.save()
			print x
			return HttpResponse(json.dumps({'message':'Successfully posted your complaint.','complaint':{'description':x.description,'user':request.user.username},'success':True}));
		else:
			return HttpResponse(json.dumps({'message':'You must be logged in to submit your complaint.','success':False}));

def searchPoliceStations(request):
	if request.method=='GET':
		location=request.GET.get('location')
		print location
		if(location=='all'):
			stations=Station.objects.all()
		else:
			stations=Station.objects.filter(locality__icontains=location)
		if stations.exists():
			stations=list(stations.values())
			return HttpResponse(json.dumps({'stations':stations,'found':True}))
		else:
			return HttpResponse(json.dumps({'found':False}))

def page_not_found(request):
	return render(request,'404.html')
