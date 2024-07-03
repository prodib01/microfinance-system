from django.shortcuts import render
from .models import Person
from loan.models import Loan
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required(login_url='login')
def guarontor_list_view(request):
    guarantors = Person.objects.all()
    return render(request, 'pages/guarantors.html', {'guarantors': guarantors, 'active':'guarantors'})

@login_required(login_url='login')
def search_guarontor(request):
    if request.method == 'POST':
        search = request.POST['search']
        guarantors = Person.objects.filter(full_name__icontains=search)
        return render(request, 'pages/guarantors.html', {'active': 'guarantors', 'guarantors':guarantors})
    else:
        return render(request, 'pages/guarantors.html', {'active': 'guarantors', 'guarantors':guarantors})


@login_required(login_url='login')
def clients_view(request):
    clients = Person.objects.all()
    return render(request, 'pages/clients.html', {'clients': clients, 'active':'clients'})


@login_required(login_url='login')
def search_client(request):
    if request.method == 'POST':
        search = request.POST['search']
        clients = Person.objects.filter(full_name__icontains=search)
        return render(request, 'pages/clients.html', {'active': 'clients', 'clients':clients})
    else:
        return render(request, 'pages/clients.html', {'active': 'clients', 'clients':clients})

def viewclient(request, client_id):
    client = Person.objects.filter(id=client_id).first()
    client_active_loans = client.loan_set.filter(status='APPROVED').count()
    client_all_loans = client.loan_set.all().count()
    client_active_balance = client.loan_set.filter(status='APPROVED').aggregate(Sum('demanded_amount'))['demanded_amount__sum']
    all_guaranted_loans = Loan.objects.filter(guarantor=client)
    all_loans = client.loan_set.filter(client=client).order_by('-created_at')
    return render(request, 'pages/clientview.html', {'client':client, 'active_loans':client_active_loans, 'total_loans':client_all_loans, 'active_balance':client_active_balance, 'all_loans': all_loans, 'all_guaranted_loans':all_guaranted_loans})

def generate_code(number, date):
    date_numeric = int(date.strftime("%y%m%d"))
    number_str = str(number).zfill(8)
    code = f"MF-{date_numeric}{number_str}"
    return code


@login_required(login_url='login')
def add_clients_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        nationality = request.POST.get('nationality')
        nin = request.POST.get('nin')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        if Person.objects.all().count() == 0:
            code= generate_code(phone, datetime.now())
        else:
            code = generate_code(phone, Person.objects.last().created_at)
        if request.POST.get('gender') == 'male':
            gender = 'M'
        if request.POST.get('gender') == 'female':
            gender = 'F'
        date_of_birth = request.POST.get('dob')
        business = request.POST.get('business')
        if request.POST.get('MS') == 'married':
            marital_status = 'Married'
            spouse_name = request.POST.get('sName')
            spouse_phone = request.POST.get('sPhone')
            person = Person(full_name=name, nationality=nationality, nin=nin, phone=phone, email=email, gender=gender, dob=date_of_birth, business=business, address=address, marital_status=marital_status, spouse_name=spouse_name, spouse_phone=spouse_phone, client_code=code)
        else:
            marital_status = request.POST.get('MS')
            person = Person(full_name=name, nationality=nationality, nin=nin, phone=phone, email=email, gender=gender, dob=date_of_birth, business=business, address=address, marital_status=marital_status, client_code=code)
        person.save()
        clients = Person.objects.all()
        return render(request, 'pages/clients.html', {'clients': clients, 'active':'clients'})
            