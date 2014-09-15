from django.db import models

# Create your models here.

# Data model for course list
class CourseList(models.Model):
    course_id = models.CharField(max_length=6, primary_key=True)
    course_name = models.CharField(max_length=30)
    instructor = models.CharField(max_length=60)

    def __unicode__(self):
        return self.course_id

# Data model for student list
class StudentList(models.Model):
    andrew_id = models.CharField(max_length=8, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.andrew_id
