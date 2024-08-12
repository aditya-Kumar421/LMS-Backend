from rest_framework import serializers
from .models import Sector, Course, Lesson, Comment

class CommentSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.fullname', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['course','sender', 'sender_name', 'rating', 'message', 'created_at']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

        
class CourseSerializer(serializers.ModelSerializer):
    educator_name = serializers.CharField(source='educator.fullname', read_only=True)
    educator_profile = serializers.URLField(source='educator.profile_pic', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'educator', 'educator_name', 'educator_profile', 'price', 'short_description', 'thumbnail', 'time_created', 'time_updated','lessons', 'review_count', 'avg_rating', 'comments']


class SectorSerializer(serializers.ModelSerializer):
    related_course = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Course.objects.all(),
        required=False
    )
    
    class Meta:
        model = Sector
        fields = ['name', 'description', 'sector_image', 'related_course']


