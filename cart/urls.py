from django.urls import path
from .views import AddToCartView, RemoveFromCartView, GetCartCoursesView

urlpatterns = [
    path('add/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('data/', GetCartCoursesView.as_view(), name='get_cart_courses'),
]
