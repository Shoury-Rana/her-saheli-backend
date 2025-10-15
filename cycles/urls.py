from django.urls import path
from .views import CycleLogView, UnifiedPredictionView, DailyLogView, DayLogToggleView, InsightsView

urlpatterns = [
    path('', CycleLogView.as_view(), name='cycle-log'),

    # New unified prediction endpoint
    # Maps to /api/cycle/predictions/
    path('predictions/', UnifiedPredictionView.as_view(), name='cycle-predictions'),
    
    # Endpoint for aggregated insights data
    # Maps to /api/cycle/insights/
    path('insights/', InsightsView.as_view(), name='cycle-insights'),
    
    # Kept daily log view, now at a cleaner URL
    # Maps to /api/cycle/logs/<date_str>/
    path('logs/<str:date_str>/', DailyLogView.as_view(), name='daily-log'),

    # New endpoint for adding/removing a single period day
    # Maps to /api/cycle/log/<date_str>/
    path('log/<str:date_str>/', DayLogToggleView.as_view(), name='day-log-toggle'),
]