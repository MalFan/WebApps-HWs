homework4 Feedback
==================

Commit graded: a17f9b50cdf9d8c4afcd8ab0fa27c44e84a62803

### Version control - Git (10/10)

### Iterative development (25/30)

  * -2, The previous homework3 grader suggested using a OneToOneField for the Profile/User relation, however this was not implemented in homework4.

  * -3, The email confirmation pages do not seem to be based on your Grumblr design. All pages of a web app should have a unified look and feel.

  * -0, Use placeholder text for your edit page inputs...

  * Make sure to read our feedback and apply it. We are always available via Piazza if you don't understand or have a question about a specific piece of feedback!

  * Hmm... *"Welcome to Simple Address Book."...

### ORM usage (26/30)

  * -3, You should not get all instances of a model and manually filter it with a loop. This is very inefficient compared to using Django’s built in filtering (generally O(n) vs O(log n)).

  * -1, Profile stats ('likes: N, following: M, followers: P') should be accurate and can be retrieved using the QuerySet (or template feature) `count`.

  * -0, The 'Relationship' model is a little unnecessary. Instead, you can add the ManyToMany relations directly onto 'Profile', which already has a relation to User.

### Coverage of technologies (40/40)

##### Template inheritance

##### Django forms

##### Image upload and dynamic display

##### Sending email

### Validation (20/20)

  * CSRF tokens aren't needed in GET requests, such as in the search form.

### Design (0/0)

  * -0, It's unclear how to follow or block another user...

  * -0, The 'edit' button shows up when I am viewing someone else's profile...

  * Nice little animation on the 'or sign up' yo.

### Additional feedback

  * -0, The site crashes when I search from any page that is not the root ('/'), which implies there is an error with using a relative vs. absolute path in your form action URL.

---

#### Total score (121/130)

---

Graded by: Shannon Lee (sjl1@andrew.cmu.edu)

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/dfan/blob/master/grades/homework4.md
