from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError

from .models import PaidCourse
from course.models import Course
from .serializers import PaidCourseSerializer

class AddPaidCourseView(APIView):
    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if user.balence < course.price:
            return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user.balance -= course.price
            user.save()
            PaidCourse.objects.create(user=user, course=course)
        except IntegrityError:
            return Response({'error': 'Course already purchased'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'success': 'Course added to paid courses'}, status=status.HTTP_200_OK)


class GetPaidCoursesView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        try:
            user = request.user
            paid_courses = PaidCourse.objects.filter(user=user)
            serializer = PaidCourseSerializer(paid_courses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PaidCourse.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
