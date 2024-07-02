from django.shortcuts import render 
from loan.models import Loan
  
def index(request): 
    return render(request, 'index.html')

def loans(request):
    loans = Loan.objects.all()
    return render(request, 'pages/loans.html', {'active': 'loans', 'loans':loans})

def search_loan(request):
    if request.method == 'POST':
        search = request.POST['search']
        loans = Loan.objects.filter(client__full_name__icontains=search)
        return render(request, 'pages/loans.html', {'active': 'loans', 'loans':loans})
    else:
        return render(request, 'pages/loans.html', {'active': 'loans', 'loans':loans})

def reports(request):
    rejected_loans = Loan.objects.filter(status='REJECTED').count()
    approved_loans = Loan.objects.filter(status='APPROVED').count()
    pending_loans = Loan.objects.filter(status='PENDING').count()
    return render(request, 'pages/reports.html', {'active': 'reports', 'loan_count':[]})

def test(request):
    return render(request, 'pages/test.html')

def sec_page(request):
    return render(request, 'pages/secPage.html')    