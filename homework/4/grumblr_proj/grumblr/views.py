from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from models import *
from forms import *

@transaction.atomic
@login_required
def homepage(request):
	context = {}

	# Get current user first
	context['current_user'] = request.user
	# Get all grumbls
	grumbls = Grumbl.get_grumbls_others(request.user)
	# context['grumbls'] = grumbls # Need to be deleted, take care of htmls

	context['grumbl_combos'] = []
	# Get all comments for each grumbl
	for grumbl in grumbls:
		comments = Comment.get_comments(grumbl)
		num_comments = len(comments)
		num_dislikes = len(grumbl.dislike_list.all())
		grumbl_combo = {'grumbl':grumbl, 
				'comments':comments, 
				'num_comments':num_comments,
				'num_dislikes':num_dislikes}
		context['grumbl_combos'].append(grumbl_combo)

	context['form_grumbl'] = GrumblForm()
	context['form_comment'] = CommentForm()
	return render(request, 'homepage.html', context)


@login_required
def my_grumbls(request):
	context = {}

	# Get current user first
	context['current_user'] = request.user
	# Store forms for HTML files
	context['form_grumbl'] = GrumblForm()
	context['form_comment'] = CommentForm()

	grumbls = Grumbl.get_grumbls_self(request.user)
	context['grumbl_combos'] = []
	# Get all comments for each grumbl
	for grumbl in grumbls:
		comments = Comment.get_comments(grumbl)
		num_comments = len(comments)
		num_dislikes = len(grumbl.dislike_list.all())
		grumbl_combo = {'grumbl':grumbl, 
				'comments':comments, 
				'num_comments':num_comments,
				'num_dislikes':num_dislikes}
		context['grumbl_combos'].append(grumbl_combo)

	return render(request, 'my-grumbls.html', context)


@transaction.atomic
@login_required
def add_grumbl(request, next):
	# Handle POST requests and then redirect.

	form_grumbl = GrumblForm(request.POST)
	# Validates the form. Error info contained in the context.
	if not form_grumbl.is_valid():
		return render(request, 'homepage.html', context)

	# If we get valid data from the form, save it.
	new_grumbl = Grumbl(text=form_grumbl.cleaned_data['grumbl'], user=request.user)
	new_grumbl.save()

	return redirect(next)


@transaction.atomic
@login_required
def add_comment(request, grumbl_id, next):
	# Handle POST requests and then redirect.
	
	form_comment = CommentForm(request.POST)

	# Validates the form. Error info contained in the context.
	if not form_comment.is_valid():
		return render(request, 'homepage.html', context) # always invalid here.

	# Get the parent grumbl via g_id
	errors = []
	try:
		parent_grumbl = Grumbl.objects.get(id=grumbl_id)
		# If we get valid data from the form, save it.
		new_comment = Comment(text=form_comment.cleaned_data['grumbl_comment'], 
								 user=request.user,
								 grumbl=parent_grumbl)
		new_comment.save()
	except ObjectDoesNotExist:
		errors.append('The grumbl did not exist.')

	# Prevent from reposting via refreshing the page.
	return redirect(next)


@login_required
def dislike(request, grumbl_id, next):
	# Get the parent grumbl via g_id
	errors = []
	try:
		parent_grumbl = Grumbl.objects.get(id=grumbl_id)
		current_user = request.user
		if current_user in parent_grumbl.dislike_list.all():
			parent_grumbl.dislike_list.remove(current_user)
		else:
			parent_grumbl.dislike_list.add(current_user)
	except ObjectDoesNotExist:
		errors.append('The grumbl did not exist.')

	return redirect(next)


@login_required
def search(request):
	context = {}
	errors = []

	# Get current user first
	context['current_user'] = request.user

	# Prevent from sending mal-formed data
	if not 'search-content' in request.GET or not request.GET['search-content']:
		errors.append('Search content is required.')
		return render(request, 'homepage.html', context)

	search_content = request.GET['search-content']
	context['search_content'] = search_content

	context['grumbls'] = Grumbl.search_grumbls(search_content)

	return render(request, 'search.html', context)


@transaction.atomic
@login_required
def  profile(request):
	context = {}

	# Get current user first
	context['current_user'] = request.user

	# current_profile = Profile.objects.filter(user = request.user) # request.user need to be modified
	current_profile = Profile.objects.get(user=request.user)
	# Update num_grumbls in Profile class
	current_profile.num_grumbls = Grumbl.objects.filter(user=request.user).count()
	current_profile.save()

	context['current_profile'] = current_profile
	# context['current_profile_name'] = request.user

	return render(request, 'profile.html', context)


@login_required
def  edit_profile(request):
	# BIG UPDATE
	context = {}
	# Get current user first
	context['current_user'] = request.user

	profile_to_edit = get_object_or_404(Profile, user=request.user)

	if request.method == 'GET':
		form_profile = ProfileForm(instance=profile_to_edit)
		context['form_profile'] = form_profile
		return render(request, 'editprofile.html', context)
	else:
		# If method is POST
		form_profile = ProfileForm(request.POST, instance=profile_to_edit) # Won't conflict?

		if not form_profile.is_valid():
			context['form_profile'] = form_profile
			return render(request, 'editprofile.html', context)

		form_profile.save()
		return redirect('/profile')
	# BIG UPDATE

	# current_profile = Profile.objects.get(user=request.user)
	# context['current_profile'] = current_profile
	# # context['current_profile_name'] = request.user
	# return render(request, 'editprofile.html', context)


@transaction.atomic
def register(request):
	context = {}

	# Just display the registration form if it is a GET request
	if request.method == 'GET':
		context['form_registration'] = RegistrationForm()
		return render(request, 'register.html', context)
	else:
		# Creates a bound form from the request POST parameters and makes the 
		# form available in the request context dictionary.
		form_registration = RegistrationForm(request.POST)
		context['form_registration'] = form_registration

		# Validates the form.
		if not form_registration.is_valid():
		    return render(request, 'register.html', context)

		# If we get here the form data was valid.  Register and login the user.
		new_user = User.objects.create_user(username=form_registration.cleaned_data['username'],
											    email = form_registration.cleaned_data['email'],
		                                    			    password=form_registration.cleaned_data['password1'])
		new_user.save()
		# Create a profile for the new user at the same time.
		new_user_profile = Profile(user = new_user)
		new_user_profile.save()

		# Logs in the new user and redirects to his/her todo list
		new_user = authenticate(username=form_registration.cleaned_data['username'],
								    email = form_registration.cleaned_data['email'],
		                              	    password=form_registration.cleaned_data['password1'])
		login(request, new_user)
		return redirect('/')



