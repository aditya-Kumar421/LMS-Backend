from django.db import models
from django.conf import settings
from course.models import Course  

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return f"Cart of {self.user.username}"