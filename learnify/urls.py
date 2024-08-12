from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('course/', include('course.urls')),
    path('mycourses/', include('myCourses.urls')),
    path('cart/', include('cart.urls')),
]