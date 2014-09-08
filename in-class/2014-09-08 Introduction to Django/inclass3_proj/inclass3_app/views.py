from django.shortcuts import render

# Create your views here.
# The action for the 'inclass3_app/hello-world' route.
def create_student(request):
    return render(request, 'create-student.html', {})

def create_course(request):
    return render(request, 'create-course.html', {})

def register(request):
    return render(request, 'register.html', {})

def students_list(request):
    context = {}
    context['person_name'] = ''
    
    if 'person_name' in request.GET:
        context['person_name'] = request.GET['person_name']
    return render(request, 'students-list.html', context)

def enrolled_list(request):
    context = {}
    context['person_name'] = ''
    context['course_name'] = ''
        
    if 'person_name' in request.GET:
        context['person_name'] = request.GET['person_name']
    if 'course_name' in request.GET:
        context['course_name'] = request.GET['course_name']
        
    return render(request, 'enrolled-list.html', context)