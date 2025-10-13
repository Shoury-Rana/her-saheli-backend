from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CycleViewSet, DailyLogView, MenstrualPredictionView, TTCPredictionView

router = DefaultRouter()
router.register(r'menstrual/periods', CycleViewSet, basename='cycle')

urlpatterns = [
    path('', include(router.urls)),
    path('menstrual/logs/<str:date_str>/', DailyLogView.as_view(), name='daily-log'),
    path('menstrual/prediction/', MenstrualPredictionView.as_view(), name='menstrual-prediction'),
    path('ttc/prediction/', TTCPredictionView.as_view(), name='ttc-prediction'),
]