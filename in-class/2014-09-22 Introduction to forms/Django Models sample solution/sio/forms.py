from django import forms

from django.contrib.auth.models import User
from models import *

# Inside this file, we usually do some validation for text 
# inputed in the form

class CreateStudent(forms.Form):
	andrew_id = forms.CharField(max_length = 20)
    	first_name = forms.CharField(max_length = 40)
	last_name = forms.CharField(max_length = 40)
	tel_number = forms.CharField(max_length=13)
	zip_code = forms.CharField(max_length=6)

	def clean(self):
		# Calls our parent (forms.Form) .clean function, gets a dictionary
		# of cleaned data as a result
		cleaned_data = super(CreateStudent, self).clean()

		# Generally return the cleaned data we got from our parent.
		return cleaned_data

	def clean_andrew_id(self):
		# Confirms that the username is not already present in the
		# User model database.
		andrew_id = self.cleaned_data.get('andrew_id')
		if Student.objects.filter(andrew_id__exact=andrew_id):
		    raise forms.ValidationError("Already created this student.")
		# Generally return the cleaned data we got from the cleaned_data
		# dictionary
		return andrew_id

	# def clean_tel_number(self):
	# 	# Confirms that the username is not already present in the
	# 	# User model database.
	# 	tel_number = self.cleaned_data.get('tel_number')
	# 	if Student.objects.filter(andrew_id__exact=andrew_id):
	# 	    raise forms.ValidationError("Already created this student.")
	# 	# Generally return the cleaned data we got from the cleaned_data
	# 	# dictionary
	# 	return andrew_id


class CreateCourse(forms.Form):
	course_number = forms.CharField(max_length = 20)
    	course_name = forms.CharField(max_length = 255)
	instructor = forms.CharField(max_length = 255)

	def clean(self):
		# Calls our parent (forms.Form) .clean function, gets a dictionary
		# of cleaned data as a result
		cleaned_data = super(CreateCourse, self).clean()

		# Generally return the cleaned data we got from our parent.
		return cleaned_data

	def clean_course_number(self):
		# Confirms that the username is not already present in the
		# User model database.
		course_number = self.cleaned_data.get('course_number')
		if Course.objects.filter(course_number__exact=course_number):
		    raise forms.ValidationError("Already created this course.")

		# Generally return the cleaned data we got from the cleaned_data
		# dictionary
		return course_number


class RegisterStudent(forms.Form):
	andrew_id = forms.CharField(max_length = 20)
	course_number = forms.CharField(max_length = 20)	

	def clean(self):
		# Calls our parent (forms.Form) .clean function, gets a dictionary
		# of cleaned data as a result
		cleaned_data = super(RegisterStudent, self).clean()

		andrew_id = self.cleaned_data.get('andrew_id')
		course_number = self.cleaned_data.get('course_number')

		if Student.objects.filter(andrew_id__exact=andrew_id) and Course.objects.filter(course_number__exact=course_number):
			course = Course.objects.get(course_number=course_number)
			student = Student.objects.get(andrew_id=andrew_id)
			if student in course.students.all():
				raise forms.ValidationError("This student has already registered this course.")

		# Generally return the cleaned data we got from our parent.
		return cleaned_data

	def clean_andrew_id(self):
		# Confirms that the username is not already present in the
		# User model database.
		andrew_id = self.cleaned_data.get('andrew_id')
		if not Student.objects.filter(andrew_id__exact=andrew_id):
		    raise forms.ValidationError("Cannot find this student.")
		# Generally return the cleaned data we got from the cleaned_data
		# dictionary
		return andrew_id

	def clean_course_number(self):
		# Confirms that the username is not already present in the
		# User model database.
		course_number = self.cleaned_data.get('course_number')
		if not Course.objects.filter(course_number__exact=course_number):
		    raise forms.ValidationError("Cannot find this course")

		# Generally return the cleaned data we got from the cleaned_data
		# dictionary
		return course_number