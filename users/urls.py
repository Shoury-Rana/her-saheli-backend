from django.urls import path
from .views import UserRegistrationView, UserProfileView, LogoutView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
]