from django.urls import path
from .views import home_view, welcome_view, make_deposit,search_guarantors

urlpatterns = [
    path('', welcome_view, name='home'),
    path('home/', home_view, name='home'),
    path('make-deposit', make_deposit, name='make-deposit'),
    path('search-guarantors/', search_guarantors, name='search-guarantors'),
]