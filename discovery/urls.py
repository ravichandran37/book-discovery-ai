from django.urls import path
from .views import DiscoveryAPIView

urlpatterns = [
    path('ask/', DiscoveryAPIView.as_view(), name='ask_ai'),
]