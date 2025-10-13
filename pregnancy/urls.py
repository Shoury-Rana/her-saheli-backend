from django.urls import path
from .views import PregnancyProfileView

urlpatterns = [
    path('profile/', PregnancyProfileView.as_view(), name='pregnancy-profile'),
]