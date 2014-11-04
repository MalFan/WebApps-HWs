from django.test import TestCase, Client
from models import *

class GrumblrModelsTest(TestCase):
    def test_simple_add(self):
        self.assertTrue(User.objects.all().count() == 0)
        new_user = User(username='testuser', password='test', email='test@andrew.cmu.edu')
        new_user.save()
        self.assertTrue(User.objects.all().count() == 1)
        self.assertTrue(User.objects.filter(username__contains='test'))
        

# class GrumblrGrumblTest(TestCase):
#                                 # Seeds the test database with data we obtained
#     fixtures = ['grumblr']  # from python manage.py dumpdata 

#     def test_home_page(self):   # Tests that a GET request to /shared-todo-list/
#         client = Client()       # results in an HTTP 200 (OK) response.
#         response = client.get('/')
#         self.assertEqual(response.status_code, 200)


#     def test_post_grumbl(self):    # Tests the to-do list add-item function.
#         client = Client()       # add-item expects a POST request with one
#                                 # query parameter, item, the text of the to-do
#                                 # list item.
#         sample_grumbl_text = 'This is a test of posting a grumbl'
#         response = client.post('/add-grumbl/homepage', {'item':sample_item})
#         self.assertTrue(response.content.find(sample_item) >= 0)



