from django.urls import path
from .views import ClientViewSet

urlpatterns = [
    path('clients/', ClientViewSet.as_view(), name='clients_api'),
]