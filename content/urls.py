from django.urls import path
from .views import StaticContentView

urlpatterns = [
    path('', StaticContentView.as_view(), name='static-content-list'),
]