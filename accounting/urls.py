from django.urls import path
from .views import journalentries

urlpatterns = [
    path('journalentries/<int:account_id>/', journalentries, name='journalentries'),
]