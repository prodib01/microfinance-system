from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from clientApp.models import Person
from loan.models import LoanProduct, SecurityType, Loan, Deposit, LoanAmortization, Penalty
from homeApp.models import Notification
from dateutil.relativedelta import relativedelta
from loan.views import calculate_loan_payment
from django.db import models
from django.http import JsonResponse
import datetime

def welcome_view(request):
    return render(request, 'index.html')

def all_loans_about_to_expire():
    loans = Loan.objects.filter(status='APPROVED')
    date_today = datetime.datetime.now().date()
    for loan in loans:
        loan_amortizations = LoanAmortization.objects.filter(loan=loan)
        for loan_amortization in loan_amortizations:
            if loan_amortization.payment_date.date() == date_today:
                if loan_amortization.status == "PENDING":
                    if Notification.objects.filter(loan=loan).count() == 0:
                        Notification.objects.create(loan=loan, title='Loan Expiry', message='A loan by ' + loan.client.full_name + ' is about to expire. Please take necessary action.')
            if date_today >= loan_amortization.payment_date.date():
                if loan_amortization.status == "PENDING":
                    if Notification.objects.filter(loan=loan).count() == 0:
                        Notification.objects.create(loan=loan, title='Loan Expiry', message='A loan by ' + loan.client.full_name + ' expired by ' + loan_amortization.payment_date.strftime('%d, %a, %b, %Y') + ' and it is beyond pament. Please take necessary action.')
                    else:
                        notification = Notification.objects.filter(loan=loan).first()
                        notification.message = 'A loan by ' + loan.client.full_name + ' expired by ' + loan_amortization.payment_date.strftime('%d, %a, %b, %Y') + ' and it is beyond pament. Please take necessary action.'
                        notification.save()

@login_required(login_url='login')
def search_guarantors(request):
    query = request.GET.get('q', '')
    if query:
        people = Person.objects.filter(full_name__icontains=query)
        results = [{'id': person.id, 'text': f"{person.full_name} - {person.nin}"} for person in people]
    else:
        results = []
    return JsonResponse(results, safe=False)

@login_required(login_url='login')
def home_view(request):
    people = Person.objects.all()
    all_loans_about_to_expire()
    loan_products = LoanProduct.objects.all()
    security_types = SecurityType.objects.all()
    active_loans = Loan.objects.filter(status='APPROVED').order_by('-approved_at')[:4]
    approved_loans = Loan.objects.filter(status='APPROVED').count() or 0
    total_amount_approved_loans = Loan.objects.filter(status='APPROVED').aggregate(total_amount=models.Sum('given_amount'))['total_amount'] or 0
    today = datetime.datetime.now().date()
    total_amount_given_today = Loan.objects.filter(status='APPROVED', approved_at=datetime.datetime.now().date()).aggregate(total_amount=models.Sum('given_amount'))['total_amount'] or 0
    user_type = request.user.profile.role
    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')
    penalty = Penalty.objects.all().first()
    context = {
        'people': people,
        'loan_products': loan_products,
        'security_types': security_types,
        'active': 'home',
        'active_loans': active_loans,
        'approved_loans': approved_loans,
        'total_amount_approved_loans': total_amount_approved_loans,
        'total_amount_given_today': total_amount_given_today,
        'user_type': user_type,
        'notifications': notifications,
        'penalty': (penalty.percentage/100) if penalty else '0'
    }
    return render(request, 'pages/home.html', context)


def make_deposit(request):
    if request.method == 'POST':
        loan_id = request.POST.get('loan')
        person_id = request.POST.get('person')
        amount = float(request.POST.get('amount'))
        deposit_made_at = request.POST.get('date')
        loan = Loan.objects.filter(id=loan_id).first()
        person = Person.objects.filter(id=person_id).first()
        amount += float(person.account_balance)
        person.account_balance = 0
        
        loan_amortizations = LoanAmortization.objects.filter(loan=loan) 
        penalty = Penalty.objects.all().first() 
        for loan_amortization in loan_amortizations:
            if loan_amortization.payment_date < datetime.datetime.strptime(deposit_made_at, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc):
                if loan.demanded_amount <= 0:                
                    break
                if loan_amortization.status == 'PENDING':
                    if amount >= (loan_amortization.principal + loan_amortization.interest + (loan_amortization.principal * penalty.percentage / 100)):
                        days_in_arreas = (datetime.datetime.strptime(deposit_made_at, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc) - loan_amortization.payment_date).days
                        days_in_arreas = int(days_in_arreas)
                        Deposit.objects.create(loan=loan, deposit=(loan_amortization.principal + loan_amortization.interest + (loan_amortization.principal * penalty.percentage / 100 * days_in_arreas)), deposited_at=deposit_made_at, interest=int(loan.interest_rate), ammortization=loan_amortization, previous_balance=loan.demanded_amount)
                        amount -= (loan_amortization.principal + loan_amortization.interest + (loan_amortization.principal * penalty.percentage / 100))
                        loan.demanded_amount -= (loan_amortization.principal + loan_amortization.interest)
                        loan_amortization.status = 'PAID'
                        loan_amortization.save()
                        loan.save()
                    else:
                        person.account_balance += amount
                        person.save()
                        amount = 0
            elif loan_amortization.payment_date == datetime.datetime.strptime(deposit_made_at, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc):
                if loan.demanded_amount <= 0:                
                    break
                if loan_amortization.status == 'PENDING':
                    if amount >= (loan_amortization.principal + loan_amortization.interest):
                        Deposit.objects.create(loan=loan, deposit=(loan_amortization.principal + loan_amortization.interest + (loan_amortization.principal * penalty.percentage / 100)), deposited_at=deposit_made_at, interest=int(loan.interest_rate), ammortization=loan_amortization, previous_balance=loan.demanded_amount)
                        amount -= (loan_amortization.principal + loan_amortization.interest)
                        loan.demanded_amount -= (loan_amortization.principal + loan_amortization.interest)
                        loan_amortization.status = 'PAID'
                        loan_amortization.save()
                        loan.save()
            else:
                person.account_balance += amount
                person.save()
                amount = 0 
    return redirect('/home')