from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Cart
from course.models import Course
from .serializers import CartSerializer, AddCourseToCartSerializer, RemoveCourseFromCartSerializer

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request):
        serializer = AddCourseToCartSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.validated_data['course_id']
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart.courses.add(course)
            cart.save()
            return Response({'message': 'Course added to cart'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request):
        serializer = RemoveCourseFromCartSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.validated_data['course_id']
            try:
                cart = Cart.objects.get(user=request.user)
                cart.courses.remove(course)
                cart.save()
                return Response({'message': 'Course removed from cart'}, status=status.HTTP_200_OK)
            except Cart.DoesNotExist:
                return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetCartCoursesView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
