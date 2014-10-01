from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class Grumbl(models.Model):
	text = models.CharField(max_length=42)
	user = models.ForeignKey(User)
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
		return reversed(grumbls)
	@staticmethod
	def get_grumbls_self(user):
		grumbls = Grumbl.objects.filter(user=user)
		return reversed(grumbls)
	@staticmethod
	def search_grumbls(search_content):
		grumbls = Grumbl.objects.filter(text__contains=search_content)
		return reversed(grumbls)


class GrumblComment(models.Model):
	comment = models.CharField(max_length=42)
	user = models.ForeignKey(User)
	grumbl = models.ForeignKey(Grumbl)
	pub_time = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
	user = models.ForeignKey(User)
	follower_list = models.ManyToManyField(User)
	grumbl = models.ForeignKey(Grumbl)
	pub_time = models.DateTimeField(auto_now_add=True)



class Profile(models.Model):
	user = models.ForeignKey(User)
	intro = models.CharField(max_length=200, default='What do you want to say?',
			blank=True)
	location = models.CharField(max_length=50, default='Where are you?', 
			blank=True)
	num_grumbls = models.IntegerField(default=0)

	# avatar = models.ImageField()

	def __unicode__(self):
		return self.user
