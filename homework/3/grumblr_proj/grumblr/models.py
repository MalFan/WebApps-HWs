from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class Grumbl(models.Model):
	text = models.CharField(max_length=42)
	user = models.ForeignKey(User)
	pub_time = models.DateTimeField(auto_now=True)
	likes = models.IntegerField(default=0)
	dislikes = models.IntegerField(default=0)
	# img = models.ImageField()

	def __unicode__(self):
		return self.text

class Profile(models.Model):
	username = models.CharField(max_length=30)
	location = models.CharField(max_length=50)
	intro = models.CharField(max_length=200)

	# avatar = models.ImageField()

	def __unicode__(self):
		return self.username
