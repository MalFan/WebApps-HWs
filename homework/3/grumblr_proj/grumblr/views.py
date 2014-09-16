from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from grumblr.models import *

@login_required
def homepage(request):
	# Sets up list of just the logged-in user's (request.user's) grumbls
	# grumbls = Grumbl.objects.all()
	grumbls = Grumbl.objects.filter(user = request.user)
	return render(request, 'homepage.html', {'grumbls': grumbls})

@login_required
def  profile(request):
	# current_profile = Profile.objects.filter(username = request.user) # request.user need to be modified
	return render(request, 'profile.html', {})

@login_required
def  edit_profile(request):
	return render(request, 'editprofile.html', {})

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

	# Logs in the new user and redirects to his/her todo list
	new_user = authenticate(username = request.POST['username'], \
							    email = request.POST['email'], \
							    password = request.POST['password1'])
	login(request, new_user)
	return redirect('homepage.html')


