from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsEducator
from .models import Sector, Course, Lesson, Comment
from .serializers import SectorSerializer, CourseSerializer, LessonSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Q


class CoursesHomeView(APIView):
    def get(self, request, *args, **kwargs):
        sectors = Sector.objects.order_by("?")[:6]

        sector_response = []

        for sector in sectors:
            sector_courses = sector.related_course.order_by("?")[:4]
            courses_serializer = CourseSerializer(sector_courses, many=True)
    
            sector_obj = {
                "sector_name": sector.name,
                "sector_id": sector.id,
                "featured_course": courses_serializer.data,
            }

            sector_response.append(sector_obj)

        return Response(data=sector_response, status=status.HTTP_200_OK)

class SectorAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            sector = get_object_or_404(Sector, pk=pk)
            serializer = SectorSerializer(sector)
        else:
            sectors = Sector.objects.all()
            serializer = SectorSerializer(sectors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SectorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        sector = get_object_or_404(Sector, pk=pk)
        serializer = SectorSerializer(sector, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        sector = get_object_or_404(Sector, pk=pk)
        sector.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CourseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            course = get_object_or_404(Course, pk=pk)
            serializer = CourseSerializer(course)
        else:
            courses = Course.objects.all()
            serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class CoursePostAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEducator]

    def post(self, request):
        request.data['educator'] = request.user.id
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            course.update_review_statistics() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            course.update_review_statistics()  # Update review stats after update
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LessonAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            lesson = get_object_or_404(Lesson, pk=pk)
            serializer = LessonSerializer(lesson)
        else:
            lessons = Lesson.objects.all()
            serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        serializer = LessonSerializer(lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AddComment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            course = Course.objects.get(id=id)
        except Course.DoesNotExist:
            return Response("Course not found.", status=status.HTTP_404_NOT_FOUND)

        content = request.data
        if not content.get("message"):
            return Response("Message field is required.", status=status.HTTP_400_BAD_REQUEST)

        content['sender'] = request.user.id
        
        serializer = CommentSerializer(data=content)
        if serializer.is_valid():
            comment = serializer.save()
            course.update_review_statistics() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class SearchCourse(APIView):

    def get(self, request, search_term):
        matches = Course.objects.filter(Q(title__icontains=search_term))
        serializer = CourseSerializer(matches, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
