from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class Grumbl(models.Model):
	text = models.CharField(max_length=42)
	user = models.ForeignKey(User)
	pub_time = models.DateTimeField(auto_now_add=True)
	dislike_list = models.ManyToManyField(User, related_name='dislike_list')
	picture = models.ImageField(upload_to='grumbl-pics', null='True', blank='True')

	def __unicode__(self):
		return self.text

	@staticmethod
	def get_grumbls_others(current_user):
		grumbls = Grumbl.objects.filter(user__follow_list__user__username__contains=current_user.username).exclude(user__block_list__user__username__contains=current_user.username).order_by('id').reverse()
		return grumbls
	@staticmethod
	def get_new_grumbls_others(current_user, grumbl_id):
		grumbl_id = int(grumbl_id)
		grumbls = Grumbl.objects.filter(id__gt=grumbl_id).filter(user__follow_list__user__username__contains=current_user.username).exclude(user__block_list__user__username__contains=current_user.username).order_by('id')
		return grumbls
	@staticmethod
	def get_grumbls_self(current_user):
		grumbls = Grumbl.objects.filter(user=current_user).order_by('id').reverse()
		return grumbls
	@staticmethod
	def search_grumbls(search_content):
		grumbls = Grumbl.objects.filter(text__contains=search_content).order_by('id').reverse()
		return grumbls

class Comment(models.Model):
	text = models.CharField(max_length=42) 
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
		profiles = Profile.objects.filter(user__username__contains=search_content)
		return profiles
