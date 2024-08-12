from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from cloudinary.models import CloudinaryField
from user.models import User
from django.conf import settings


class Sector(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    related_course = models.ManyToManyField('Course', blank=True)
    sector_image = CloudinaryField('image', blank=False, null=True)
    
    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    educator = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(null=True, blank=False)
    short_description = models.CharField(max_length=200, null=True, blank=True)
    thumbnail = CloudinaryField('image', blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    review_count = models.PositiveIntegerField(null=True, default=0)
    avg_rating = models.FloatField(validators=[MaxValueValidator(5), MinValueValidator(0)], default=0)

    def __str__(self):
        return self.title
    
    def update_review_statistics(self):
        comments = self.comments.all()
        self.review_count = comments.count()
        if self.review_count > 0:
            total_rating = sum(comment.rating for comment in comments)
            self.avg_rating = total_rating / self.review_count
        else:
            self.avg_rating = 0
        self.save()


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    lesson_name = models.TextField(max_length=200, null=True)
    video = models.FileField(
        upload_to="courses/videos",
        null=True,
        blank=True,
        storage=VideoMediaCloudinaryStorage(),
    )
    length = models.CharField(max_length=100, default="")
    time = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.course) + " - " + str(self.lesson_name[0:25])

class Comment(models.Model):
    course = models.ForeignKey(Course, related_name='comments', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MaxValueValidator(5), MinValueValidator(0)], default=0)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.sender.fullname} on {self.course}"

