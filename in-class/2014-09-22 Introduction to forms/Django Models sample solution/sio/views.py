from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from models import *
from forms import *

def home(request):
    context = {}
    context['form_student'] = CreateStudent()
    context['form_course'] = CreateCourse()
    context['form_register'] = RegisterStudent()
    context['courses'] = Course.objects.all()
    return render(request, 'sio.html', context)

@transaction.atomic
def create_student(request):
    context = {}
    messages = []
    context['form_course'] = CreateCourse()
    context['form_register'] = RegisterStudent()

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form_student = CreateStudent(request.POST)
    context['form_student'] = form_student

    # Validates the form.
    if not form_student.is_valid():
        messages.append('Invalidate student data. Please check.')
        context['messages'] = messages
        context['courses'] = Course.objects.all()
        return render(request, 'sio.html', context)

    # If we get here the form data was valid.  Create the student.
    new_student = Student(andrew_id=form_student.cleaned_data['andrew_id'], 
                                         first_name=form_student.cleaned_data['first_name'],
                                         last_name=form_student.cleaned_data['last_name'])
    new_student.save()

    messages.append('Added %s' % new_student)
    context['messages'] = messages

    context['courses'] = Course.objects.all()

    return render(request, 'sio.html', context)

@transaction.atomic
def create_course(request):
    context = {}
    messages = []
    context['form_student'] = CreateStudent()
    context['form_register'] = RegisterStudent()

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form_course = CreateCourse(request.POST)
    context['form_course'] = form_course

    # Validates the form.
    if not form_course.is_valid():
        messages.append('Invalidate course data. Please check.')
        context['messages'] = messages
        context['courses'] = Course.objects.all()
        return render(request, 'sio.html', context)

    # If we get here the form data was valid.  Create the student.
    new_course = Course(course_number=form_course.cleaned_data['course_number'], 
                                       course_name=form_course.cleaned_data['course_name'],
                                       instructor=form_course.cleaned_data['instructor'])
    new_course.save()

    messages.append('Added %s' % new_course)
    context['messages'] = messages

    context['courses'] = Course.objects.all()

    return render(request, 'sio.html', context)

@transaction.atomic
def register_student(request):
    context = {}
    messages = []
    context['form_student'] = CreateStudent()
    context['form_course'] = CreateCourse()
    # if Student.objects.filter(andrew_id=request.POST['andrew_id']).count() != 1:
    #     messages.append("Could not find Andrew ID %s." %
    #                     request.POST['andrew_id'])
    # if Course.objects.filter(course_number=request.POST['course_number']).count() != 1:
    #     messages.append("Could not find course %s." %
    #                     request.POST['course_number'])

    # if messages:
    #     return make_view(request, messages)

    form_register = RegisterStudent(request.POST)
    context['form_register'] = form_register

    # Validates the form.
    if not form_register.is_valid():
        messages.append('Invalidate registration data. Please check.')
        context['messages'] = messages
        context['courses'] = Course.objects.all()
        return render(request, 'sio.html', context)

    course = Course.objects.get(course_number=request.POST['course_number'])
    student = Student.objects.get(andrew_id=request.POST['andrew_id'])
    course.students.add(student)
    course.save()

    messages.append('Added %s to %s' % (student, course))
    context['messages'] = messages

    context['courses'] = Course.objects.all()

    return render(request, 'sio.html', context)
