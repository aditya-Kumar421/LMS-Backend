from django.contrib import admin
from .models import User


@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ('username','fullname', 'email', 'role')
    list_filter = ('fullname', 'email')
    search_fields = ('fullname', 'email', 'role')

    