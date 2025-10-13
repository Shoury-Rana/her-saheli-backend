from django.urls import path
from .views import PostpartumMoodLogView

urlpatterns = [
    path('logs/<str:date_str>/', PostpartumMoodLogView.as_view(), name='postpartum-log'),
]