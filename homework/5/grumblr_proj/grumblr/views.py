from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from django.core import serializers
from django.http import HttpResponse

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required
# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import *

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
		context = {}
		errors = 'invalid input. Note that you cannot post an empty grumbl.'
		context['errors'] = errors
		return render(request, 'homepage.html', context)

	# If we get valid data from the form, save it.
	new_grumbl = Grumbl(text=form_grumbl.cleaned_data['grumbl'], user=request.user)
	new_grumbl.save()

	return redirect(next)


@transaction.atomic
@login_required
def add_comment(request, grumbl_id):
	# Handle POST requests and then redirect.

	form_comment = CommentForm(request.POST)

	# Validates the form. Error info contained in the context.
	if not form_comment.is_valid():
		context = {}
		errors = 'invalid input. Note that you cannot post an empty comment.'
		context['errors'] = errors
		# return redirect('/')
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

	response_text = serializers.serialize('json', [new_comment])

    	return HttpResponse(response_text, content_type='application/json')


@login_required
def dislike(request, grumbl_id):
	# Get the parent grumbl via g_id
	errors = []
	try:
		parent_grumbl = Grumbl.objects.get(id=grumbl_id)
		current_user = request.user
		if current_user in parent_grumbl.dislike_list.all():
			parent_grumbl.dislike_list.remove(current_user)
			response_text = -1
		else:
			parent_grumbl.dislike_list.add(current_user)
			response_text = 1	
	except ObjectDoesNotExist:
		errors.append('The grumbl did not exist.')

	return HttpResponse(response_text)


@login_required
def block(request, user_id):
	# Get the user via u_id
	
	try:
		target_user = User.objects.get(id=user_id)
		current_user = request.user
		if target_user in current_user.profile.block_list.all():
			current_user.profile.block_list.remove(target_user)
		else:
			current_user.profile.block_list.add(target_user)
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
		if target_user in current_user.profile.follow_list.all():
			current_user.profile.follow_list.remove(target_user)
		else:
			current_user.profile.follow_list.add(target_user)
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
			if target_user in current_user.profile.follow_list.all():
				current_user.profile.follow_list.remove(target_user)
			else:
				current_user.profile.follow_list.add(target_user)
		except ObjectDoesNotExist:
			errors = []
			errors.append('The user did not exist.')
		return redirect('myfollowing')

	# Get current user first
	current_user = request.user
	context['current_user'] = current_user

	follow_list = current_user.profile.follow_list.all()
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
			if target_user in current_user.profile.block_list.all():
				current_user.profile.block_list.remove(target_user)
			else:
				current_user.profile.block_list.add(target_user)
		except ObjectDoesNotExist:
			errors = []
			errors.append('The user did not exist.')
		return redirect('myblocking')

	# Get current user first
	current_user = request.user
	context['current_user'] = current_user

	block_list = current_user.profile.block_list.all()
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
	current_user = request.user
	context['current_user'] = current_user
	target_user = User.objects.get(id=user_id)

	context['form_search'] = SearchForm() 

	target_profile = Profile.objects.get(user=target_user)

	context['target_profile'] = target_profile
	context['target_profile_num_grumbls'] = Profile.get_num_grumbls(target_user)
	num_dislikes = 0
	for grumbl in Grumbl.objects.all():
		if current_user == grumbl.user:
			num_dislikes += grumbl.dislike_list.count()
	context['target_profile_num_dislikes'] = num_dislikes
	context['target_profile_num_followings'] = current_user.profile.follow_list.all().count()
	context['target_profile_num_followers'] = current_user.follow_list.all().count()

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

    		# Generate a one-time use token and an email message body
    		token = default_token_generator.make_token(new_user)	

		email_body = """
Welcome to grumblr. Please click the link below to
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


@login_required
def my_password_change(request, *args, **kwargs):
	return password_change(request,
		template_name='change-password.html',
		post_change_redirect='password_change_done',
		password_change_form=ChangePasswordForm,
		current_app=None,
		extra_context={'current_user':request.user,
		'form_search':SearchForm()})


@login_required
def my_password_change_done(request, *args, **kwargs):
	return password_change_done(request,
		template_name='password-change-confirmation.html',
		current_app=None,
		extra_context={'current_user':request.user,
		'form_search':SearchForm()})


def my_password_reset(request, *args, **kwargs):
	return password_reset(request,
		is_admin_site=None,
		template_name='password_reset_form.html',
		email_template_name='password_reset_email.html',
		password_reset_form=ResetPasswordForm,
		# token_generator=None,
		post_reset_redirect='password_reset_done',
		# from_email=None,
		current_app=None,
		extra_context=None#,
		# html_email_template_name=None
		)


def my_password_reset_done(request, *args, **kwargs):
	return password_reset_done(request,
		template_name='password_reset_done.html',
		current_app=None,
		extra_context=None)


@login_required
def refresh(request):

	current_grumbl_id = request.GET['grumblid']
	current_username = request.GET['username']

	current_user=User.objects.get(username=current_username)
	grumbls = Grumbl.get_grumbls_others(request.user)
	grumbls = grumbls[::-1]

	grumbl_user = []
	for grumbl in grumbls:
		if int(grumbl.id) > int(current_grumbl_id):
			print grumbl.id
			grumbl_user.append(grumbl)
			grumbl_user.append(grumbl.user)

	response_text = serializers.serialize('json', grumbl_user)

    	return HttpResponse(response_text, content_type='application/json')




	# # context = {}

	# # Get current user first
	# context['current_user'] = request.user
	# # Get all grumbls
	# grumbls = Grumbl.get_grumbls_others(request.user)
	# # context['grumbls'] = grumbls # Need to be deleted, take care of htmls

	# context['grumbl_combos'] = []
	# # Get all comments for each grumbl
	# for grumbl in grumbls:
	# 	comments = Comment.get_comments(grumbl)
	# 	num_comments = len(comments)
	# 	num_dislikes = len(grumbl.dislike_list.all())
	# 	grumbl_combo = {'grumbl':grumbl, 
	# 			'comments':comments, 
	# 			'num_comments':num_comments,
	# 			'num_dislikes':num_dislikes}
	# 	context['grumbl_combos'].append(grumbl_combo)

	# context['form_grumbl'] = GrumblForm()
	# context['form_comment'] = CommentForm()
	# context['form_search'] = SearchForm()
	# return render(request, 'homepage.html', context)



	# # Get the parent grumbl via g_id
	# errors = []
	# try:
	# 	parent_grumbl = Grumbl.objects.get(id=grumbl_id)
	# 	current_user = request.user
	# 	if current_user in parent_grumbl.dislike_list.all():
	# 		parent_grumbl.dislike_list.remove(current_user)
	# 		response_text = -1
	# 	else:
	# 		parent_grumbl.dislike_list.add(current_user)
	# 		response_text = 1	
	# except ObjectDoesNotExist:
	# 	errors.append('The grumbl did not exist.')

	# return HttpResponse(response_text)





	# form_comment = CommentForm(request.POST)

	# # Validates the form. Error info contained in the context.
	# if not form_comment.is_valid():
	# 	context = {}
	# 	errors = 'invalid input. Note that you cannot post an empty comment.'
	# 	context['errors'] = errors
	# 	return None
	# 	# return redirect('/')
	# 	# return render(request, 'homepage.html', context) # always invalid here.

	# # Get the parent grumbl via g_id
	# errors = []
	# try:
	# 	parent_grumbl = Grumbl.objects.get(id=grumbl_id)
	# 	# If we get valid data from the form, save it.
	# 	new_comment = Comment(text=form_comment.cleaned_data['grumbl_comment'], 
	# 							 user=request.user,
	# 							 grumbl=parent_grumbl)
	# 	new_comment.save()
	# except ObjectDoesNotExist:
	# 	errors.append('The grumbl did not exist.')

	# response_text = serializers.serialize('json', [new_comment])

 #    	return HttpResponse(response_text, content_type='application/json')