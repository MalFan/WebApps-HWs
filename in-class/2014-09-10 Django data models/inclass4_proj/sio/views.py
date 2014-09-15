from django.shortcuts import render

# Imports the StudentList & CourseList class
from sio.models import *

# Action for the default sio/ route.
def home(request):

	# render takes: (1) the request,
	#               (2) the name of the view to generate, and
	#               (3) a dictionary of name-value pairs of data to be
	#                   available to the view.
	return render(request, 'sio.html', {})


# Action for the sio/create-student route.
def create_student(request):
	errors = []  # A list to record messages for any errors we encounter.

	# Adds the new item to the database if the request parameter is present
	if not 'andrew-id' in request.POST or not request.POST['andrew-id'] or not 'first-name' in request.POST or not request.POST['first-name'] or not 'last-name' in request.POST or not request.POST['last-name']:
		errors.append('You must enter student information.')
    	else:
		new_student = StudentList(andrew_id = request.POST['andrew-id'],
					              first_name = request.POST['first-name'],
					              last_name = request.POST['last-name'])
		new_student.save()

	# Sets up data needed to generate the view, and generates the view
	students = StudentList.objects.all()
	context = {'students':students, 'errors':errors}
	return render(request, 'create-student.html', context)


# Action for the sio/create-course route.
def create_course(request):
	errors = []  # A list to record messages for any errors we encounter.

	# Adds the new item to the database if the request parameter is present
	if not 'course-id' in request.POST or not request.POST['course-id'] or not 'course-name' in request.POST or not request.POST['course-name'] or not 'instructor' in request.POST or not request.POST['instructor']:
		errors.append('You must enter course information.')
    	else:
		new_course = CourseList(course_id = request.POST['course-id'],
					              course_name = request.POST['course-name'],
					              instructor = request.POST['instructor'])
		new_course.save()

	# Sets up data needed to generate the view, and generates the view
	courses = CourseList.objects.all()
	context = {'courses':courses, 'errors':errors}
	return render(request, 'create-course.html', context)


# Action for the sio/register route.
def register(request):
	context = {}
	context['andrew_id'] = ''
	context['course_id'] = ''

	# Sets up data needed to generate the view, and generates the view
	if 'andrew-id' in request.POST:
    		context['andrew_id'] = request.POST['andrew-id']
    	if 'course-number' in request.POST:
     		context['course_id'] = request.POST['course-number']
	return render(request, 'register.html', context)

