from django.urls import path
from .views import SectorAPIView, CourseAPIView, LessonAPIView, CoursesHomeView, AddComment, SearchCourse, CoursePostAPIView

urlpatterns = [
    path('sectors/', SectorAPIView.as_view()),
    path('sectors/<int:pk>/', SectorAPIView.as_view()),
    path('homesector/', CoursesHomeView.as_view()),
    path('courses/', CourseAPIView.as_view()),
    path('coursesChange/', CoursePostAPIView.as_view()),
    path('courses/<int:pk>/', CourseAPIView.as_view()),
    path('lessons/', LessonAPIView.as_view()),
    path('lessons/<int:pk>/', LessonAPIView.as_view()),
    path('comment/<int:id>/', AddComment.as_view()),
    path("search/<str:search_term>/", SearchCourse.as_view()),
]
