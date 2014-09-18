from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from grumblr.models import *

from django.db import transaction

@transaction.atomic
@login_required
def homepage(request):
	context = {}
	errors = []

	# Get current user first
	context['current_user'] = request.user

	# Sets up list of just the logged-in user's (request.user's) grumbls
	# Just display the homepage if it is a GET request
	if request.method == 'GET':
		grumbls = Grumbl.objects.all()
		# grumbls = Grumbl.objects.filter(user = request.user)
		context['grumbls'] = reversed(grumbls)
		return render(request, 'homepage.html', context)
	
	# If it is a POST request, process that request first
	if not 'grumble-text' in request.POST or not request.POST['grumble-text']:
		errors.append('You must enter an item to add.')
	else:
		new_grumbl = Grumbl(text=request.POST['grumble-text'], user=request.user)
		new_grumbl.save()

	# grumbls = Grumbl.objects.filter(user=request.user)
	grumbls = Grumbl.objects.all()
	context['grumbls'] = reversed(grumbls)
	context['errors'] = errors

	return render(request, 'homepage.html', context)

@login_required
def my_grumbls(request):
	context = {}

	# Get current user first
	context['current_user'] = request.user

	grumbls = Grumbl.objects.filter(user=request.user)
	# grumbls = Grumbl.objects.all()
	context['grumbls'] = reversed(grumbls)

	# There is another page--mygrumbls.html, but it is not in use for now
	return render(request, 'homepage.html', context) 


@login_required
def search(request):
	context = {}
	errors = []

	# Get current user first
	context['current_user'] = request.user

	if not 'search-content' in request.GET or not request.GET['search-content']:
		errors.append('Username is required.')
		return render(request, 'homepage.html', context)
	else:
		search_content = request.GET['search-content']
		context['search_content'] = search_content

	grumbls = Grumbl.objects.filter(text__contains=search_content)
	# grumbls = Grumbl.objects.all()
	context['grumbls'] = reversed(grumbls)

	return render(request, 'search.html', context)

@transaction.atomic
@login_required
def  profile(request):
	context = {}
	errors = []

	# Get current user first
	context['current_user'] = request.user

	# If it is a POST request, process that request first
	if request.method == 'POST':
		if not 'intro' in request.POST or not 'location' in request.POST:
			errors.append('Invalid changes is made.')
			context['errors'] = errors
			return render(request, 'editprofile.html', context)
		else:
			current_profile = Profile.objects.get(user=request.user)
			current_profile.intro = request.POST['intro']
			current_profile.location = request.POST['location']
			current_profile.save()
		
	# current_profile = Profile.objects.filter(user = request.user) # request.user need to be modified
	current_profile = Profile.objects.get(user=request.user)
	context['current_profile'] = current_profile
	# context['current_profile_name'] = request.user

	return render(request, 'profile.html', context)

@login_required
def  edit_profile(request):
	context = {}

	# Get current user first
	context['current_user'] = request.user

	current_profile = Profile.objects.get(user=request.user)
	context['current_profile'] = current_profile
	# context['current_profile_name'] = request.user
	return render(request, 'editprofile.html', context)

@transaction.atomic
def register(request):
	context = {}

	# Just display the registration form if it is a GET request
	if request.method == 'GET':
		return render(request, 'register.html', context)

	errors = []
	context['errors'] = errors

	# Check the validity of the form data
	# Check if the param 'username' is submitted or if 'username' is non-empty
	if not 'username' in request.POST or not request.POST['username']:
		errors.append('Username is required.')
	else:
		# Save the username in the request context to re-fill the username
		# field in case the form has errors
		context['username'] = request.POST['username']

	if not 'email' in request.POST or not request.POST['email']:
		errors.append('Email is required.')

	if not 'password1' in request.POST or not request.POST['password1']:
		errors.append('Password is required.')
	if not 'password2' in request.POST or not request.POST['password2']:
		errors.append('Confirm password is required.')

	if 'password1' in request.POST and 'password2' in request.POST \
	  and request.POST['password1'] and request.POST['password2'] \
	  and request.POST['password1'] != request.POST['password2']:
		errors.append('Password did not match.')

	if len(User.objects.filter(username = request.POST['username'])) > 0:
		errors.append('Username is already taken.')

	if errors:
		return render(request, 'register.html', context)

	# Creates the new user from the valid form data
	new_user = User.objects.create_user(username = request.POST['username'], \
										    email = request.POST['email'], \
										    password = request.POST['password1'])
	new_user.save()
	new_user_profile = Profile(user = new_user)
	new_user_profile.save()

	# Logs in the new user and redirects to his/her todo list
	new_user = authenticate(username = request.POST['username'], \
							    email = request.POST['email'], \
							    password = request.POST['password1'])
	login(request, new_user)
	return redirect('/')


