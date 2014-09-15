from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^home$', 'sio.views.home'),
    # will add routes later for add student / add course / register actions
    url(r'^create-student$', 'sio.views.create_student'),
    url(r'^create-course$', 'sio.views.create_course'),
    url(r'^register$', 'sio.views.register'),
)
