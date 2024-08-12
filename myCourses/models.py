from django.db import models
from django.conf import settings
from course.models import Course  

class PaidCourse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paid_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Courses of {self.user.fullname}"
    
    class Meta:
        unique_together = ('user', 'course')