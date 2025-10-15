from django.urls import path
from .views import CycleLogView, UnifiedPredictionView, DailyLogView

urlpatterns = [
    path('', CycleLogView.as_view(), name='cycle-log'),

    # New unified prediction endpoint
    # Maps to /api/cycle/predictions/
    path('predictions/', UnifiedPredictionView.as_view(), name='cycle-predictions'),
    
    # Kept daily log view, now at a cleaner URL
    # Maps to /api/cycle/logs/<date_str>/
    path('logs/<str:date_str>/', DailyLogView.as_view(), name='daily-log'),
]