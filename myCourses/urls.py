from django.urls import path
from .views import *

urlpatterns = [
    path('add/<int:course_id>/', AddPaidCourseView.as_view(), name='add_to_paid_course'),
    path('data/', GetPaidCoursesView.as_view(), name='get_paid_courses'),
]
