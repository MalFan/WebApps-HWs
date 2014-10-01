homework3 Feedback
==================

Commit graded: f34fe878f953ad961c1e2bd42934d70529d55e01

### Version control - Git (10/10)

### Iterative design (10/10)

### Implementation and functionality (80/85)

##### Routing and configuration (urls.py/settings.py)

##### Models (models.py)
  * -0 We suggest using a OneToOneField to a user because there should only be one instance of this object per user. Selecting the correct relation is important for database performance.

##### Views (views.py)
  * -5, other user’s profiles cannot be accessed through links
  * -0, There's no way to change my password or my email

##### Authentication

##### Templates
  * -0, Make sure you don't print out `__all__` with your errors.
  * -0, Your errors on the login page are difficult to read.
  * -0, Be sure to delete commented-out code from your templates.

### Additional feedback
  * You should use placeholder text for your edit page inputs.
  * I'd recommending making user's names be links almost any time they appear
  

---

#### Total score (100/105)

---

Graded by: Salem Hilal (salem@cmu.edu)

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/dfan/blob/master/grades/homework3.md
