from django.urls import path
from .views import UserRegistrationView, UserProfileView, LogoutView, MyTokenObtainPairView

urlpatterns = [
    # URLs to match frontend expectations
    path('register/', UserRegistrationView.as_view(), name='auth_register'),
    path('login/', MyTokenObtainPairView.as_view(), name='auth_login'),
    
    # Kept original names for internal consistency if needed
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
]