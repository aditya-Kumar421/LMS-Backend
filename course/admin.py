from django.contrib import admin
from .models import Sector, Course, Lesson, Comment


@admin.register(Sector)
class Sector(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Course)
class Course(admin.ModelAdmin):
    list_display = ('title','price')
    list_filter = ('title', 'price')
    search_fields = ('title',)
    
admin.site.register(Comment)
admin.site.register(Lesson)