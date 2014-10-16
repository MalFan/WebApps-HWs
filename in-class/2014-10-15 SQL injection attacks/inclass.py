courses = Course.objects.filter(students__first_name__exact='Shannon')
stu_list = []
for course in courses:
    students = course.students.exclude(first_name__exact='Shannon')
    for student in students:
        stu_list.append(student)

