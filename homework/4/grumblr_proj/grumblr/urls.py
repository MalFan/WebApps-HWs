from django.conf.urls import patterns, include, url
from django.contrib import admin
from forms import *

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'grumblr_proj.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),
	url(r'^$', 'grumblr.views.homepage', name='home'),
	url(r'^my-grumbls$', 'grumblr.views.my_grumbls', name='mygrumbls'),
	url(r'^search$', 'grumblr.views.search', name='search'),

	url(r'^profile$', 'grumblr.views.profile'),
	url(r'^edit-profile$', 'grumblr.views.edit_profile', name='editprofile'),

	# Route for built-in authentication with our own custom login page
	url(r'^login$', 'django.contrib.auth.views.login', 
		{'template_name':'login.html', 
		'authentication_form':LoginForm}, name='login'),
	# Route to log out a user and send them back to the login page
	url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
	url(r'^register$', 'grumblr.views.register', name='register'),
)
