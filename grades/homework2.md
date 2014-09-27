homework2 Feedback
==================

Commit graded: 3a393a446c56527beb4a8b858f1e8821e311c063

### Routing and configuration (20/20)

Good job!

### Calculator functionality (15/20)

-5, Your calculator crashes on a string input in the hidden field. The error is "invalid literal for int() with base 10: 'wood'" See https://github.com/CMU-Web-Application-Development/dfan/blob/c18983e8d5b899bd9edf4efa33744344ecbecf84/homework/2/HW2/calc/views.py#L19 If the int method is called on a string which is not a number, it will throw an error.

Your calculator crashes on a string entered as a button value. The error was a UnboundedLocaError as a result of "local variable 'btn_clicked_type' referenced before assignment". See https://github.com/CMU-Web-Application-Development/dfan/blob/37a4faaa1c14f06f948dcea3e7b9e0574f9afe31/homework/2/HW2/calc/views.py#L37-L47. You can see if a button value does not match a type that you specified in the if and elif statements, it will crash when trying to reference 'btn_clicked_type'.

The application should not crash as a result of any client provided information. You shouldn't assume that clients will always send input in the format that you specify. HTTP requests can be easily forged.

### Calculator implementation (20/20)

Good job!

### Version control - Git (4/5)

-1, Commits should represent incremental changes. For example, a majority of your submission is within your first commit. This could have been broken up into multiple commits each with a detailed message.

### Additional feedback

---

#### Total score (59/65)

---

Graded by: Eliot Wong (eliotw@cmu.edu)

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/dfan/blob/master/grades/homework2.md
