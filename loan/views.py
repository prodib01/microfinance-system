from django.shortcuts import render, redirect
from django.http import JsonResponse
import datetime
from dateutil.relativedelta import relativedelta
from .models import Loan, LoanProduct, SecurityType, LoanImage, Remarks, LoanAmortization, Document, Deposit, LoanGuarantor
from clientApp.models import Person
from branch.models import Branch
from homeApp.models import Notification
from .serializers import LoanAmortizationSerializer, LoanSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Prefetch


def calculate_loan_payment(principal, monthly_interest_rate, loan_term_years, payment_frequency='weekly', start_date=datetime.date.today()):
    annual_interest_rate = monthly_interest_rate * 12
    if payment_frequency in ['weekly', 'bi-weekly']:
        periodic_interest_rate = annual_interest_rate / 52
        if payment_frequency == 'bi-weekly':
            payments_per_year = 26
        else:
            payments_per_year = 52
    elif payment_frequency == 'daily':
        periodic_interest_rate = annual_interest_rate / 365
        payments_per_year = 365
    elif payment_frequency == 'monthly':
        periodic_interest_rate = annual_interest_rate / 12
        payments_per_year = 12
    elif payment_frequency == 'quarterly':
        periodic_interest_rate = annual_interest_rate / 4
        payments_per_year = 4
    elif payment_frequency == 'yearly':
        periodic_interest_rate = annual_interest_rate
        payments_per_year = 1
    else:
        raise ValueError(
            "Invalid payment frequency. Please use 'weekly', 'bi-weekly', 'daily', 'monthly', 'quarterly', or 'yearly'.")

    # Calculate total number of payments
    total_payments = loan_term_years * payments_per_year
    total_payments = int(total_payments)

    # Calculate periodic payment amount using reducing balance formula
    periodic_payment = principal * \
        (periodic_interest_rate) / \
        (1 - (1 + periodic_interest_rate)**(-total_payments))

    # Generate amortization schedule with payment dates
    amortization_schedule = []
    remaining_balance = principal
    payment_date = start_date
    days_between_payments = 365 / payments_per_year
    for i in range(total_payments):
        interest_payment = remaining_balance * periodic_interest_rate
        principal_payment = periodic_payment - interest_payment
        remaining_balance -= principal_payment
        amortization_schedule.append(
            (i+1, periodic_payment, interest_payment, principal_payment, remaining_balance, payment_date))
        # Update payment date for the next payment
        if payment_frequency == 'daily':
            payment_date += datetime.timedelta(days=1)
        elif payment_frequency == 'weekly':
            payment_date += datetime.timedelta(weeks=1)
        elif payment_frequency == 'bi-weekly':
            payment_date += datetime.timedelta(weeks=2)
        elif payment_frequency == 'monthly':
            payment_date += relativedelta(months=1)
        elif payment_frequency == 'quarterly':
            payment_date += relativedelta(months=3)
        elif payment_frequency == 'semi-annually':
            payment_date += relativedelta(months=6)
        elif payment_frequency == 'yearly':
            payment_date += relativedelta(years=1)

    total_interest = sum([entry[2] for entry in amortization_schedule])

    return periodic_payment, amortization_schedule, total_payments, total_interest, periodic_interest_rate


def calculate_loan_request(request):
    if request.method == 'POST':
        principal = int(request.POST.get('principal'))
        monthly_interest_rate = int(request.POST.get('annual_interest_rate'))
        annual_interest_rate_to_return = monthly_interest_rate
        monthly_interest_rate = monthly_interest_rate / 100
        loan_term_number = int(request.POST.get('loan_term_number'))
        loan_term_type_of_period = request.POST.get('loan_term_type_of_period')
        payment_frequency = request.POST.get('payment_frequency')
        # start_date = datetime.date.today() + relativedelta(months=1)

        if loan_term_type_of_period == 'years':
            loan_term_years = loan_term_number
        elif loan_term_type_of_period == 'months':
            loan_term_years = loan_term_number / 12
        elif loan_term_type_of_period == 'weeks':
            loan_term_years = loan_term_number / 52
        elif loan_term_type_of_period == 'days':
            loan_term_years = loan_term_number / 365
        else:
            raise ValueError(
                "Invalid loan term type of period. Please use 'years', 'months', 'weeks', or 'days'.")

        if payment_frequency == 'weekly':
            start_date = datetime.date.today() + relativedelta(weeks=1)
        elif payment_frequency == 'bi-weekly':
            start_date = datetime.date.today() + relativedelta(weeks=2)
        elif payment_frequency == 'daily':
            start_date = datetime.date.today() + datetime.timedelta(days=1)
        elif payment_frequency == 'monthly':
            start_date = datetime.date.today() + relativedelta(months=1)
        elif payment_frequency == 'quarterly':
            start_date = datetime.date.today() + relativedelta(months=3)
        elif payment_frequency == 'semi-annually':
            start_date = datetime.date.today() + relativedelta(months=6)
        elif payment_frequency == 'yearly':
            start_date = datetime.date.today() + relativedelta(years=1)
        else:
            raise ValueError(
                "Invalid payment frequency. Please use 'weekly', 'bi-weekly', 'daily', 'monthly', 'quarterly', or 'yearly'.")

        periodic_payment, amortization_schedule, total_payments, total_interest, periodic_interest_rate = calculate_loan_payment(
            principal, monthly_interest_rate, loan_term_years, payment_frequency, start_date)

        amortization_schedule = [
            {
                'payment_number': entry[0],
                'payment': round(entry[1]),
                'interest': round(entry[2]),
                'principal': round(entry[3]),
                'remaining_balance': round(entry[4]),
                'payment_date': entry[5].strftime('%d, %a, %b, %Y')
            }
            for entry in amortization_schedule
        ]

        return JsonResponse({
            'installment': round(periodic_payment),
            'amortization_schedule': amortization_schedule,
            'status': 'success',
            'principal': principal,
            # monthly interest rate is gotten by dividing the annual interest rate by 12 months, so it means that it is a must for the user to input the annual interest rate
            'annual_interest_rate': annual_interest_rate_to_return,
            'loan_term_years': loan_term_years,
            'payment_frequency': payment_frequency,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'total_payments': total_payments,
            'total_interest': round(total_interest),
            'periodic_interest_rate': round(periodic_interest_rate)
        })


def add_loan_request(request):
    if request.method == 'POST':
        client_id = request.POST.get('client')
        loan_product_id = request.POST.get('loanProduct')
        requested_amount = request.POST.get('requestedAmount')
        recommended_amount = request.POST.get('recommendedAmount')
        loan_term_number = request.POST.get('loanTermNumber')
        loan_term_type_of_period = request.POST.get('loanTermTypeOfPeriod')
        payment_frequency = request.POST.get('paymentFrequency')
        security_type_id = request.POST.get('securityType')
        security_description = request.POST.get('securityDescription')
        security_image = request.FILES.get('securityImage2')
        guarantor = request.POST.getlist('guarantor[]')
        guarantor_relationship = request.POST.get('guarantorRelationship')

        client = Person.objects.filter(id=client_id).first()
        loan_product = LoanProduct.objects.filter(id=loan_product_id).first()
        security_type = SecurityType.objects.filter(
            id=security_type_id).first()
        guarantors = Person.objects.filter(id__in=guarantor)

        loan = Loan()
        loan.client = client
        loan.loan_product = loan_product
        loan.requested_amount = requested_amount
        loan.recommended_amount = recommended_amount
        loan.loan_term = loan_term_number
        loan.loan_term_type_of_period = loan_term_type_of_period
        loan.payment_frequency = payment_frequency
        loan.security_type = security_type
        loan.security_description = security_description
        loan.guarantor = guarantor
        loan.guarantor_relationship = guarantor_relationship
        loan.interest_rate = 20
        loan.branch = request.user.profile.branch
        loan.loan_officer = request.user.profile
        loan.approved_at = datetime.datetime.now()
        loan.save()

        for guarantor in guarantors:
            loan_guarantor = LoanGuarantor()
            loan_guarantor.loan = loan
            loan_guarantor.guarantor = guarantor
            loan_guarantor.guarantee = client
            loan_guarantor.save()

        notification = Notification()
        notification.loan = loan
        notification.title = 'Loan Request'
        notification.message = f'A new loan request has been made by {client.full_name}.'
        notification.save()

        if security_image:
            loan_image = LoanImage()
            loan_image.loan = loan
            loan_image.image = security_image
            loan_image.save()

        return redirect('requests')


def load_requests(request):
    loan_guarantors = LoanGuarantor.objects.select_related(
        "guarantor", "guarantee"
    ).all()
    loan_requests = Loan.objects.prefetch_related(
        Prefetch("loanguarantor_set", queryset=loan_guarantors)
    ).all()
    for loan in loan_requests:
        print(loan.loanguarantor_set.all())
    rejected_loans = Loan.objects.filter(status="REJECTED").count()
    approved_loans = Loan.objects.filter(status="APPROVED").count()
    pending_loans = Loan.objects.filter(status="PENDING").count()
    remarks = Remarks.objects.all()
    branches = Branch.objects.all()
    user = request.user
    return render(
        request,
        "pages/requests.html",
        {
            "user": user,
            "loan_requests": loan_requests,
            "active": "requests",
            "loan_count": [rejected_loans, pending_loans, approved_loans],
            "remarks": remarks,
            "branches": branches,
        },
    )


def accept_loan(request, loan_id):
    if request.user.profile.role == "BUSINESS_SUPERVISOR":
        loan_requests = Loan.objects.all()
        loan = Loan.objects.filter(id=loan_id).first()
        remark = request.POST.get('remark')
        remarks = Remarks()
        remarks.loan = loan
        remarks.remarks = remark
        remarks.created_by = request.user.profile
        remarks.save()

        notification = Notification()
        notification.title = 'Loan Remarked'
        notification.loan = loan
        notification.message = f'A loan request has been remarked for {loan.client.full_name}.'
        notification.save()
    else:
        loan_requests = Loan.objects.all()
        loan = Loan.objects.filter(id=loan_id).first()
        amount = request.POST.get('amount')
        rate = request.POST.get('rate')
        dod = request.POST.get('dod')
        branch = request.POST.get('disbursementbranch')
        disbursement_branch = Branch.objects.filter(id=branch).first()
        duration_num = request.POST.get('loanTermNumber')
        duration_type = request.POST.get('loanTermTypeOfPeriod')
        loan.given_amount = int(amount)
        loan.disbursment_branch = disbursement_branch
        loan.interest_rate = rate
        loan.loan_term = duration_num
        loan.approved_at = dod
        loan.loan_term_type_of_period = str(duration_type).lower()
        loan.status = 'APPROVED'

        principal = int(amount)
        annual_interest_rate = int(rate)
        annual_interest_rate = annual_interest_rate / 100
        loan_term_number = int(duration_num)
        loan_term_type_of_period = duration_type
        payment_frequency = loan.payment_frequency

        if loan_term_type_of_period == 'years':
            loan_term_years = loan_term_number
        elif loan_term_type_of_period == 'months':
            loan_term_years = loan_term_number / 12
        elif loan_term_type_of_period == 'weeks':
            loan_term_years = loan_term_number / 52
        elif loan_term_type_of_period == 'week':
            loan_term_years = loan_term_number / 52
        elif loan_term_type_of_period == 'days':
            loan_term_years = loan_term_number / 365
        else:
            raise ValueError(
                "Invalid loan term type of period. Please use 'years', 'months', 'weeks', or 'days'.")

        if payment_frequency == 'weekly':
            start_date = datetime.datetime.strptime(
                loan.approved_at, '%Y-%m-%d') + relativedelta(weeks=1)
        elif payment_frequency == 'bi-weekly':
            start_date = datetime.datetime.strptime(
                loan.approved_at, '%Y-%m-%d') + relativedelta(weeks=2)
        elif payment_frequency == 'daily':
            start_date = datetime.datetime.strptime(
                loan.approved_at, '%Y-%m-%d') + datetime.timedelta(days=1)
        elif payment_frequency == 'monthly':
            start_date = datetime.datetime.strptime(
                loan.approved_at, '%Y-%m-%d') + relativedelta(months=1)
        elif payment_frequency == 'quarterly':
            start_date = datetime.datetime.strptime(
                loan.approved_at, '%Y-%m-%d') + relativedelta(months=3)
        elif payment_frequency == 'semi-annually':
            start_date = datetime.datetime.strptime(
                loan.approved_at, '%Y-%m-%d') + relativedelta(months=6)
        elif payment_frequency == 'yearly':
            start_date = datetime.datetime.strptime(
                loan.approved_at, '%Y-%m-%d') + relativedelta(years=1)
        else:
            raise ValueError(
                "Invalid payment frequency. Please use 'weekly', 'bi-weekly', 'daily', 'monthly', 'quarterly', or 'yearly'.")

        periodic_payment, amortization_schedule, total_payments, total_interest, periodic_interest_rate = calculate_loan_payment(
            principal, annual_interest_rate, loan_term_years, payment_frequency, start_date)
        loan.unit_interest = round(periodic_interest_rate)
        loan.installment = round(periodic_payment)
        loan.account_interest = round(total_interest)
        loan.demanded_amount = round(loan.given_amount + total_interest)
        loan.save()
        amortization_schedule = [
            {
                'payment_number': entry[0],
                'payment': round(entry[1]),
                'interest': round(entry[2]),
                'principal': round(entry[3]),
                'remaining_balance': round(entry[4]),
                'payment_date': entry[5].strftime('%d, %a, %b, %Y')
            }
            for entry in amortization_schedule
        ]

        for entry in amortization_schedule:
            loan_amortization = LoanAmortization()
            loan_amortization.loan = loan
            loan_amortization.payment_date = datetime.datetime.strptime(
                entry['payment_date'], "%d, %a, %b, %Y").strftime("%Y-%m-%d")
            loan_amortization.principal = entry['payment']
            loan_amortization.status = 'PENDING'
            loan_amortization.interest = entry['interest']
            loan_amortization.ending_balance = entry['remaining_balance']
            loan_amortization.save()

        notification = Notification()
        notification.title = 'Loan Approved'
        notification.loan = loan
        notification.message = f'A loan request has been approved for {loan.client.full_name}.'
        notification.save()
    return redirect('/loan', {'loan_requests': loan_requests, 'active': 'requests'})


def reject_loan(request, loan_id):
    loan_requests = Loan.objects.all()
    loan = Loan.objects.filter(id=loan_id).first()
    loan.status = 'REJECTED'
    loan.save()
    notification = Notification()
    notification.title = 'Loan Rejected'
    notification.loan = loan
    notification.message = f'A loan request has been rejected for {loan.client.full_name}.'
    notification.save()
    return redirect('/loan', {'loan_requests': loan_requests, 'active': 'requests'})


@api_view(['GET'])
def get_person_loans(request, person_id):
    person = Person.objects.filter(id=person_id).first()
    loans = Loan.objects.filter(client=person).filter(status='APPROVED')
    loan_serializer = LoanSerializer(loans, many=True).data
    for serialized_loan in loan_serializer:
        loan = Loan.objects.filter(id=serialized_loan['id']).first()
        serialized_loan['name'] = str(loan.loan_product.name) + ' - ' + str(loan.disbursment_branch.name) + ' - ' + str(
            loan.given_amount) + ' - ' + str(loan.loan_term) + loan.loan_term_type_of_period
    return Response({'loans': loan_serializer})


@api_view(['GET'])
def get_loan_ammortization(request, loan_id):
    loan = Loan.objects.filter(id=loan_id).first()
    loan_amortization = LoanAmortization.objects.filter(loan=loan)
    loan_amortization_serializer = LoanAmortizationSerializer(
        loan_amortization, many=True).data
    return Response({'loan_amortization': loan_amortization_serializer})


def loanview(request, loan_id):
    loan = Loan.objects.filter(id=loan_id).first()
    docs = Document.objects.filter(loan=loan).order_by('-id')
    ammortizations = LoanAmortization.objects.filter(loan=loan)
    for ammortization in ammortizations:
        if ammortization.payment_date.date() < datetime.datetime.now().date():
            if ammortization.status == "PENDING":
                arrear_days = (datetime.datetime.now().date() -
                               ammortization.payment_date.date()).days
                arreas = arrear_days
                ammortization.save()
                break
        else:
            arreas = 0
            break
    if loan.status != "PENDING":
        loan_inrement_by_interest_today = (
            loan.given_amount * loan.interest_rate / 100)
        loan_increment_by_interest = loan_inrement_by_interest_today * arreas
    else:
        arreas = 0
        loan_increment_by_interest = None
        loan_inrement_by_interest_today = None
    deposits = Deposit.objects.filter(loan=loan)

    loan_image = LoanImage.objects.filter(loan=loan).first()
    loan_image_url = loan_image.image.url if loan_image else None

    return render(request, 'pages/loanview.html', {
        'loan': loan,
        'docs': docs,
        'arreas': arreas,
        'loan_increment_by_interest': loan_increment_by_interest,
        'ammortizations': ammortizations,
        'deposits': deposits,
        'loan_image_url': loan_image_url
    })


def search_loan(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        loan_requests = Loan.objects.filter(
            client__full_name__icontains=search)
        rejected_loans = Loan.objects.filter(status='REJECTED').count()
        approved_loans = Loan.objects.filter(status='APPROVED').count()
        pending_loans = Loan.objects.filter(status='PENDING').count()
        remarks = Remarks.objects.all()
        branches = Branch.objects.all()
        user = request.user
        return render(request, 'pages/requests.html', {'user': user, 'loan_requests': loan_requests, 'active': 'requests', 'loan_count': [rejected_loans, pending_loans, approved_loans], 'remarks': remarks, 'branches': branches})
    else:
        return redirect('requests')


def add_doc(request, loan_id):
    loan = Loan.objects.filter(id=loan_id).first()
    doc = Document()
    doc.title = request.POST.get('title')
    doc.loan = loan
    doc.document = request.FILES['file']
    doc.save()
    return redirect('loanview', loan_id=loan_id,)
