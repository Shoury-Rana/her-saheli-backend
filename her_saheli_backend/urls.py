from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from users.views import UserProfileView # Import the view directly
from cycles.views import SymptomLogView, MoodLogView # <-- ADD THIS IMPORT

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication and User Profile URLs
    path('api/auth/', include('users.urls')),
    path('api/user/profile/', UserProfileView.as_view(), name='user-profile-detail'),

    # App URLs
    path('api/cycle/', include('cycles.urls')),
    path('api/pregnancy/', include('pregnancy.urls')),
    path('api/postpartum/', include('postpartum.urls')),
    path('api/content/', include('content.urls')),
    path('api/chatbot/', include('chatbot.urls')),
    
    #URLS FOR LOGGING 
    path('api/symptoms/', SymptomLogView.as_view(), name='log-symptoms'),
    path('api/mood/', MoodLogView.as_view(), name='log-mood'),

    # API Documentation URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]