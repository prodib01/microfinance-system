from django.contrib.auth import logout, login
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from users.models import MuroUser
from branch.models import Branch
from .models import Profile
from django.db.models import Q
from django.core.mail import send_mail


def logout_view(request):
    logout(request)
    return redirect('/')

@csrf_exempt # this should be looked at in the future
def login_view(request):
    is_error = False
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
        is_error = True
    return render(request, 'pages/login.html', {'is_error': is_error})


@login_required(login_url='login')
def search_user(request):
    if request.method == 'POST':
        search = request.POST['search']
        staffs = MuroUser.objects.filter(Q(email__icontains=search) | Q(phone_number__icontains=search))
        branches = Branch.objects.all()
        return render(request, 'pages/staff.html', {'staffs': staffs, 'branches': branches, 'active':'staff'})
    else:
        return redirect('staff')

@login_required(login_url='login')
def users_view(request):
    staffs = MuroUser.objects.all()
    branches = Branch.objects.all()
    return render(request, 'pages/staff.html', {'staffs': staffs, 'branches': branches, 'active':'staff'})


@login_required(login_url='login')
def add_staff(request):
    if request.method == 'POST':
        email = request.POST['email']
        fullname = request.POST['fullname']
        phone = request.POST['phone']
        role = request.POST['role']
        branch_id = request.POST['branch']
        password = request.POST['password']
        user_exists = MuroUser.objects.filter(
            Q(email=email) | Q(phone_number=phone)).exists()
        if user_exists:
            messages.error(
                request, 'User with email or phone number already exists')
            return redirect('staff')
        user = MuroUser.objects.create_user(
            email=email, password=password, fullname=fullname, phone_number=phone)
        branch = Branch.objects.get(id=branch_id)
        profile = Profile.objects.create(user=user, role=role, branch=branch)
        messages.success(request, 'User added successfully')
        profile.save()
        send_mail(
            'Muro Account',
            f'Your account has been created. Your password is {password}',
            'kunoomaking@gmail.com',
            [email],
            fail_silently=False,
        )
        return redirect('staff')