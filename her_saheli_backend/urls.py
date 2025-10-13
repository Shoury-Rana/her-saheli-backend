from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication URLs
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App URLs
    path('api/users/', include('users.urls')),
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