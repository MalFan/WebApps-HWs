from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class Grumbl(models.Model):
	text = models.CharField(max_length=42)
	user = models.ForeignKey(User)
	pub_time = models.DateTimeField(auto_now_add=True)
	dislike_list = models.ManyToManyField(User, related_name='dislike_list')

	def __unicode__(self):
		return self.text

	@staticmethod
	def get_grumbls_others(current_user):
		user_list = []
		follow_list = current_user.profile.follow_list.all()
		block_list = current_user.profile.block_list.all()
		for user in follow_list:
			if not user in block_list:
				user_list.append(user)
		grumbls = []
		for grumbl in Grumbl.objects.all():
			if grumbl.user in user_list:
				grumbls.append(grumbl)
		return grumbls[::-1]
	@staticmethod
	def get_grumbls_self(current_user):
		grumbls = Grumbl.objects.filter(user=current_user)
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

	def __unicode__(self):
		return self.text

	@staticmethod
	def get_comments(grumbl):
		comments = Comment.objects.filter(grumbl=grumbl)
		return comments[::-1]


class Profile(models.Model):
	user = models.OneToOneField(User)
	intro = models.CharField(max_length=200, blank=True)
	location = models.CharField(max_length=50,	blank=True)
	avatar = models.ImageField(upload_to='profile-photos', default='profile-photos/user_default.png')
	
	follow_list = models.ManyToManyField(User, related_name='follow_list', blank=True)
	block_list = models.ManyToManyField(User, related_name='block_list', blank=True)

	def __unicode__(self):
		return self.user.username

	@staticmethod
	def get_num_grumbls(user):
		grumbls = Grumbl.objects.filter(user=user)
		return len(grumbls)
	@staticmethod
	def search_grumblrs(search_content):
		users = User.objects.filter(username__contains=search_content)
		profiles = []
		for user in users:
			profile = Profile.objects.get(user=user)
			profiles.append(profile)
		return profiles


# class Relationship(models.Model):
# 	user = models.OneToOneField(User)


# 	def __unicode__(self):
# 		return self.user.username