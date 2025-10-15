from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from users.views import UserProfileView # Import the view directly

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication and User Profile URLs to match frontend
    path('api/auth/', include('users.urls')),
    path('api/user/profile/', UserProfileView.as_view(), name='user-profile-detail'),

    # Other App URLs
    path('api/cycles/', include('cycles.urls')),
    path('api/pregnancy/', include('pregnancy.urls')),
    path('api/postpartum/', include('postpartum.urls')),
    path('api/content/', include('content.urls')),
    path('api/chatbot/', include('chatbot.urls')),
    
    # API Documentation URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]