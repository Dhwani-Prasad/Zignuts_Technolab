from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    # enrollment_date = models.DateField(auto_now_add=True)
    city = models.CharField(max_length=100, default='Unknown')

    # This is write to improve the code readability and maintainability. The __str__ method is defined
    # to return the name of the student when the object is printed or displayed in the Django admin interface.
    def __str__(self):
        return self.name