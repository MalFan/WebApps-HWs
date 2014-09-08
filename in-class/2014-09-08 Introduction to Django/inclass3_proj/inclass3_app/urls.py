from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'inclass3_proj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^create-student$', 'inclass3_app.views.create_student'),
    url(r'^create-course$', 'inclass3_app.views.create_course'),
    url(r'^register$', 'inclass3_app.views.register'),
    url(r'^students-list$', 'inclass3_app.views.students_list'),
    url(r'^enrolled-list$', 'inclass3_app.views.enrolled_list'),
)
