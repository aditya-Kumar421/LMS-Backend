from rest_framework import serializers
from course.models import Course
from .models import PaidCourse
from course.serializers import CourseSerializer 

class PaidCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True) 

    class Meta:
        model = PaidCourse
        fields = ['user', 'course', 'paid_on']
        read_only_fields = ['user']