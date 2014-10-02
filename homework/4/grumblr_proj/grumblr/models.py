from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class Grumbl(models.Model):
	text = models.CharField(max_length=42)
	user = models.ForeignKey(User, related_name='grumblr_of_this_grumbl')
	pub_time = models.DateTimeField(auto_now_add=True)
	# likes = models.IntegerField(default=0)
	# dislikes = models.IntegerField(default=0)
	# img = models.ImageField()
	dislike_list = models.ManyToManyField(User)

	def __unicode__(self):
		return self.text

	@staticmethod
	def get_grumbls_others(user):
		grumbls = Grumbl.objects.all() # To be modified to render all following grumbls instead of all grumbls
		return grumbls[::-1]
	@staticmethod
	def get_grumbls_self(user):
		grumbls = Grumbl.objects.filter(user=user)
		return grumbls[::-1]
	@staticmethod
	def search_grumbls(search_content):
		grumbls = Grumbl.objects.filter(text__contains=search_content)
		return grumbls[::-1]

class Comment(models.Model):
	text = models.CharField(max_length=42) # Note that "comment" changed to "text", bugs may be raised.
	user = models.ForeignKey(User)
	grumbl = models.ForeignKey(Grumbl)
	pub_time = models.DateTimeField(auto_now_add=True)

	@staticmethod
	def get_comments(grumbl):
		comments = Comment.objects.filter(grumbl=grumbl)
		return comments[::-1]


class Profile(models.Model):
	user = models.ForeignKey(User)
	intro = models.CharField(max_length=200, default='What do you want to say?',
			blank=True)
	location = models.CharField(max_length=50, default='Where are you?', 
			blank=True)
	# num_grumbls = models.IntegerField(default=0) # TO BE deleted.

	avatar = models.ImageField(upload_to="profile-photos", blank=True)

	def __unicode__(self):
		return self.user
	@staticmethod
	def get_num_grumbls(user):
		grumbls = Grumbl.objects.filter(user=user)
		return len(grumbls)
