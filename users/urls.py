from django.urls import path
from .views import login_view, logout_view, users_view, add_staff, search_user

urlpatterns = [
    path('staff', users_view, name='staff'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('users/', add_staff, name='add_staff'),
    path('search-user/', search_user, name='search-user')
]