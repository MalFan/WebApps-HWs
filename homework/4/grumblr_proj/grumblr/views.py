from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required
# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Needed to manually create HttpResponses or raise an Http404 exception
from django.http import HttpResponse, Http404

# Helper function to guess a MIME type from a file name
from mimetypes import guess_type

# Used to send mail from within Django
from django.core.mail import send_mail
# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

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
	context['form_search'] = SearchForm()
	return render(request, 'homepage.html', context)


@login_required
def my_grumbls(request):
	context = {}

	# Get current user first
	context['current_user'] = request.user
	# Store forms for HTML files
	context['form_grumbl'] = GrumblForm()
	context['form_comment'] = CommentForm()
	context['form_search'] = SearchForm() 

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
def block(request, user_id):
	# Get the user via u_id
	
	try:
		target_user = User.objects.get(id=user_id)
		current_user = request.user
		if target_user in current_user.relationship.block_list.all():
			current_user.relationship.block_list.remove(target_user)
		else:
			current_user.relationship.block_list.add(target_user)
	except ObjectDoesNotExist:
		errors = []
		errors.append('The user did not exist.')

	return redirect('/')


@login_required
def follow(request, user_id):
	# Get the user via u_id
	
	try:
		target_user = User.objects.get(id=user_id)
		current_user = request.user
		if target_user in current_user.relationship.follow_list.all():
			current_user.relationship.follow_list.remove(target_user)
		else:
			current_user.relationship.follow_list.add(target_user)
	except ObjectDoesNotExist:
		errors = []
		errors.append('The user did not exist.')

	return redirect('/')


@login_required
def my_following(request):
	context = {}
	if request.method == 'POST':
		# Get the user via u_id
		try:
			target_user = User.objects.get(id=user_id)
			current_user = request.user
			if target_user in current_user.relationship.follow_list.all():
				current_user.relationship.follow_list.remove(target_user)
			else:
				current_user.relationship.follow_list.add(target_user)
		except ObjectDoesNotExist:
			errors = []
			errors.append('The user did not exist.')
		return redirect('myfollowing')

	# Get current user first
	current_user = request.user
	context['current_user'] = current_user

	follow_list = current_user.relationship.follow_list.all()
	profiles = []
	for user in follow_list:
		profile = Profile.objects.get(user=user)
		profiles.append(profile)

	context['profiles'] =profiles
	context['form_search'] = SearchForm()
	return render(request, 'my-following.html', context)


@login_required
def my_blocking(request):
	context = {}
	if request.method == 'POST':
		# Get the user via u_id
		try:
			target_user = User.objects.get(id=user_id)
			current_user = request.user
			if target_user in current_user.relationship.block_list.all():
				current_user.relationship.block_list.remove(target_user)
			else:
				current_user.relationship.block_list.add(target_user)
		except ObjectDoesNotExist:
			errors = []
			errors.append('The user did not exist.')
		return redirect('myblocking')

	# Get current user first
	current_user = request.user
	context['current_user'] = current_user

	block_list = current_user.relationship.block_list.all()
	profiles = []
	for user in block_list:
		profile = Profile.objects.get(user=user)
		profiles.append(profile)

	context['profiles'] =profiles
	context['form_search'] = SearchForm()
	return render(request, 'my-blocking.html', context)


@login_required
def search(request):
	context = {}

	# Get current user first
	context['current_user'] = request.user

	context['form_search'] = SearchForm()
	form_search_main = SearchForm(request.GET)
	context['form_search_main'] = form_search_main

	# search_content = request.GET['search-content']
	# context['search_content'] = search_content

	if request.GET['search_type'] == 'search_grumbls':
		context['grumbls'] = Grumbl.search_grumbls(request.GET['search_content'])
	else:
		context['grumblrs'] = Profile.search_grumblrs(request.GET['search_content'])
	
	return render(request, 'search.html', context)


@transaction.atomic
@login_required
def  profile(request, user_id):
	context = {}

	# Get current user first
	user = request.user
	context['current_user'] = user
	target_user = User.objects.get(id=user_id)

	context['form_search'] = SearchForm() 

	# current_profile = Profile.objects.filter(user = request.user) # request.user need to be modified
	target_profile = Profile.objects.get(user=target_user)

	context['target_profile'] = target_profile
	context['target_profile_num_grumbls'] = Profile.get_num_grumbls(target_user)

	return render(request, 'profile.html', context)


@login_required
def  edit_profile(request):
	# BIG UPDATE
	context = {}
	# Get current user first
	context['current_user'] = request.user

	context['form_search'] = SearchForm() 

	profile_to_edit = get_object_or_404(Profile, user=request.user)

	if request.method == 'GET':
		form_profile = ProfileForm(instance=profile_to_edit)
		context['form_profile'] = form_profile
		return render(request, 'edit-profile.html', context)
	else:
		# If method is POST
		form_profile = ProfileForm(request.POST, request.FILES, instance=profile_to_edit) # Won't conflict?

		if not form_profile.is_valid():
			context['form_profile'] = form_profile
			return render(request, 'edit-profile.html', context)

		form_profile.save()
		url = '/profile/' + str(request.user.id)
		return redirect(url)


@login_required
def  get_photo(request, username):
	profile = get_object_or_404(Profile, user=User.objects.get(username=username))
	if not profile.avatar:
		raise Http404

	content_type = guess_type(profile.avatar.name)
	return HttpResponse(profile.avatar, content_type=content_type)


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
	    	# Mark the user as inactive to prevent login before email confirmation.
    		new_user.is_active = False
		new_user.save()
		# Create a profile for the new user at the same time.
		new_user_profile = Profile(user = new_user)
		new_user_profile.save()
		# Create a relationship for the new user at the same time.
		new_user_relationship = Relationship(user = new_user)
		new_user_relationship.save()

    		# Generate a one-time use token and an email message body
    		token = default_token_generator.make_token(new_user)	

		email_body = """
		Welcome to the Simple Address Book.  Please click the link below to
		verify your email address and complete the registration of your account:

		  http://%s%s
		""" % (request.get_host(), 
		       reverse('confirm', args=(new_user.username, token)))

		send_mail(subject="Verify your email address",
		          message= email_body,
		          from_email="dfan+@andrew.cmu.edu",
		          recipient_list=[new_user.email])

		context['email'] = form_registration.cleaned_data['email']
		return render(request, 'needs-confirmation.html', context)
		    

@transaction.atomic
def confirm_registration(request, username, token):
	user = get_object_or_404(User, username=username)

	# Send 404 error if token is invalid
	if not default_token_generator.check_token(user, token):
	    raise Http404

	# Otherwise token was valid, activate the user.
	user.is_active = True
	user.save()
	return render(request, 'confirmed.html', {})





		# # Logs in the new user and redirects to his/her todo list
		# new_user = authenticate(username=form_registration.cleaned_data['username'],
		# 						    email = form_registration.cleaned_data['email'],
		#                               	    password=form_registration.cleaned_data['password1'])
		# login(request, new_user)
		# return redirect('/')



