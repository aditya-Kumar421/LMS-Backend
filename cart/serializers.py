from rest_framework import serializers
from course.models import Course
from .models import Cart
from course.serializers import CourseSerializer  # Import the CourseSerializer

class CartSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['user', 'courses', 'total_price']
        read_only_fields = ['user']

    def get_total_price(self, obj):
        return sum(course.price for course in obj.courses.all())
    

class AddCourseToCartSerializer(serializers.Serializer):
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

class RemoveCourseFromCartSerializer(serializers.Serializer):
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
