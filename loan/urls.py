from django.urls import path
from . import views

urlpatterns = [
    path('', views.load_requests, name='requests'),
    path('calculate', views.calculate_loan_request, name='calculate'),
    path('add-loan-request', views.add_loan_request, name='add-loan-request'),
    path('reject-loan-request/<int:loan_id>', views.reject_loan, name='delete-loan-request'),
    path('accept-loan/<int:loan_id>', views.accept_loan, name='accept-loan'),
    path('get-loans/<int:person_id>', views.get_person_loans, name='get-loan'),
    path('get-loan-ammortization/<int:loan_id>', views.get_loan_ammortization, name='get-loan-ammortization'),
    path('loanview/<int:loan_id>/', views.loanview, name='loanview'),
    path('search-loan/', views.search_loan, name='search-loan'),   
    path('add-doc/<int:loan_id>', views.add_doc, name='add-doc'), 
    path('arrears', views.loans_in_arrears, name='arrears'),
    path('loan-payments/<int:loan_id>', views.loan_payments, name='loan-payments'),
]