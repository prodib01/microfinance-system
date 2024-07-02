from django.urls import path
from .views import guarontor_list_view, clients_view, add_clients_view, viewclient, search_client, search_guarontor

urlpatterns = [
    path('guarantor/', guarontor_list_view, name='guarantor'),
    path('add-client',add_clients_view, name='add-client'),
    path('clientview/<int:client_id>', viewclient, name='viewclient'),
    path('', clients_view, name='clients'),
    path('search-client/', search_client, name='search-client'),
    path('search-guarantor/', search_guarontor, name='search-guarantor'),
]