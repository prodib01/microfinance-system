from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from clientApp.models import Person
from loan.models import (
    LoanProduct,
    SecurityType,
    Loan,
    Deposit,
    LoanAmortization,
    Payments,
)
from homeApp.models import Notification
from django.db import models
from django.http import JsonResponse
import datetime
from decimal import Decimal
from utilities.helpers import get_system_parameter


def welcome_view(request):
    return render(request, "index.html")


def all_loans_about_to_expire():
    loans = Loan.objects.filter(status="APPROVED")
    date_today = datetime.datetime.now().date()
    for loan in loans:
        loan_amortizations = LoanAmortization.objects.filter(loan=loan)
        for loan_amortization in loan_amortizations:
            if loan_amortization.payment_date.date() == date_today:
                if loan_amortization.status == "PENDING":
                    if Notification.objects.filter(loan=loan).count() == 0:
                        Notification.objects.create(
                            loan=loan,
                            title="Loan Expiry",
                            message="A loan by "
                            + loan.client.full_name
                            + " is about to expire. Please take necessary action.",
                        )
            if date_today >= loan_amortization.payment_date.date():
                if loan_amortization.status == "PENDING":
                    if Notification.objects.filter(loan=loan).count() == 0:
                        Notification.objects.create(
                            loan=loan,
                            title="Loan Expiry",
                            message="A loan by "
                            + loan.client.full_name
                            + " expired by "
                            + loan_amortization.payment_date.strftime("%d, %a, %b, %Y")
                            + " and it is beyond pament. Please take necessary action.",
                        )
                    else:
                        notification = Notification.objects.filter(loan=loan).first()
                        notification.message = (
                            "A loan by "
                            + loan.client.full_name
                            + " expired by "
                            + loan_amortization.payment_date.strftime("%d, %a, %b, %Y")
                            + " and it is beyond pament. Please take necessary action."
                        )
                        notification.save()


@login_required(login_url="login")
def search_guarantors(request):
    query = request.GET.get("q", "")
    if query:
        people = Person.objects.filter(full_name__icontains=query)
        results = [
            {"id": person.id, "text": f"{person.full_name} - {person.nin}"}
            for person in people
        ]
    else:
        results = []
    return JsonResponse(results, safe=False)


@login_required(login_url="login")
def home_view(request):
    people = Person.objects.all()
    all_loans_about_to_expire()
    loan_products = LoanProduct.objects.all()
    security_types = SecurityType.objects.all()
    active_loans = Loan.objects.filter(status="APPROVED").order_by("-approved_at")[:4]
    approved_loans = Loan.objects.filter(status="APPROVED").count() or 0
    total_amount_approved_loans = (
        Loan.objects.filter(status="APPROVED").aggregate(
            total_amount=models.Sum("given_amount")
        )["total_amount"]
        or 0
    )
    total_amount_given_today = (
        Loan.objects.filter(
            status="APPROVED", approved_at=datetime.datetime.now().date()
        ).aggregate(total_amount=models.Sum("given_amount"))["total_amount"]
        or 0
    )
    user_type = request.user.profile.role
    notifications = Notification.objects.filter(is_read=False).order_by("-created_at")
    penalty = get_system_parameter("PENALTY").int_value
    context = {
        "people": people,
        "loan_products": loan_products,
        "security_types": security_types,
        "active": "home",
        "active_loans": active_loans,
        "approved_loans": approved_loans,
        "total_amount_approved_loans": total_amount_approved_loans,
        "total_amount_given_today": total_amount_given_today,
        "user_type": user_type,
        "notifications": notifications,
        "penalty": (penalty / 100) if penalty else "0",
    }
    return render(request, "pages/home.html", context)


def make_deposit(request):
    if request.method == "POST":
        loan_id = request.POST.get("loan")
        person_id = request.POST.get("person")
        amount_brought = Decimal(request.POST.get("amount"))
        deposit_made_at = request.POST.get("date")
        loan = Loan.objects.filter(id=loan_id).first()
        if loan.demanded_amount <= 0:
            raise Exception("Loan fully paid")

        total_balance = amount_brought + Decimal(loan.client_loan_account_balance)
        deposit = Deposit.objects.create(
            loan=loan,
            amount_deposited=amount_brought,
            deposited_at=deposit_made_at,
            amount_found_on_account=loan.client_loan_account_balance,
        )
        deposit_made_at_dtime = datetime.datetime.strptime(
            deposit_made_at, "%Y-%m-%d"
        ).replace(tzinfo=datetime.timezone.utc)
        loan_amortizations = LoanAmortization.objects.filter(loan=loan)
        penalty = get_system_parameter("PENALTY").int_value
        if penalty:
            for loan_amortization in loan_amortizations:
                if loan_amortization.payment_date < deposit_made_at_dtime:
                    if loan_amortization.status == "PENDING":
                        days_in_arreas = int(
                            (
                                deposit_made_at_dtime - loan_amortization.penalty_date
                            ).days
                        )
                        if days_in_arreas > 0:
                            penalty_amount = Decimal(
                                loan_amortization.principal_balance
                                * penalty
                                / 100
                                * days_in_arreas
                            )
                            if total_balance < penalty_amount:
                                if total_balance > 0:
                                    penalty_paid = total_balance
                                else:
                                    raise Exception("Amount is less than 0")
                            else:
                                penalty_paid = penalty_amount
                            # use 2 decimal places
                            narration = f"Penalty of {penalty_paid.__round__(2)} was paid for {days_in_arreas} days of arrears"
                            Payments.objects.create(
                                amount=penalty_paid,
                                payment_date=deposit_made_at,
                                ammortization=loan_amortization,
                                payment_type="PENALTY",
                                narration=narration,
                                deposit=deposit,
                            )
                            total_balance -= penalty_paid
                            loan_amortization.penalty_date = deposit_made_at_dtime

                        if total_balance > 0:
                            if loan_amortization.interest_balance > 0:
                                if total_balance < loan_amortization.interest_balance:
                                    interest_paid = total_balance
                                else:
                                    interest_paid = loan_amortization.interest_balance
                                total_balance -= interest_paid
                                loan.demanded_amount -= Decimal(interest_paid)
                                old_interest_balance = (
                                    loan_amortization.interest_balance
                                )
                                new_interest_balance = old_interest_balance - Decimal(
                                    interest_paid
                                )
                                narration = f"Interest of {interest_paid.__round__(2)} was paid of the total balance of {old_interest_balance} making the new balance {new_interest_balance.__round__(2)}"
                                loan_amortization.interest_balance = (
                                    new_interest_balance
                                )

                                Payments.objects.create(
                                    amount=interest_paid,
                                    payment_date=deposit_made_at,
                                    ammortization=loan_amortization,
                                    payment_type="INTEREST",
                                    deposit=deposit,
                                    narration=narration,
                                )

                        if total_balance > 0:
                            if total_balance < loan_amortization.principal_balance:
                                principal_paid = total_balance
                            elif total_balance >= loan_amortization.principal_balance:
                                principal_paid = loan_amortization.principal_balance

                            total_balance -= principal_paid
                            loan.demanded_amount -= Decimal(principal_paid)
                            old_principal_balance = loan_amortization.principal_balance
                            new_principal_balance = old_principal_balance - Decimal(
                                principal_paid
                            )
                            narration = f"Principal of {principal_paid.__round__(2)} was paid of the total balance of {old_principal_balance} making the new balance {new_principal_balance.__round__(2)}"
                            loan_amortization.principal_balance = new_principal_balance
                            Payments.objects.create(
                                amount=principal_paid,
                                payment_date=deposit_made_at,
                                ammortization=loan_amortization,
                                payment_type="PRINCIPAL",
                                deposit=deposit,
                                narration=narration,
                            )

                        if (
                            loan_amortization.principal_balance == 0
                            and loan_amortization.interest_balance == 0
                        ):
                            loan_amortization.status = "PAID"

                        loan_amortization.save()

            loan.client_loan_account_balance = total_balance
            loan.save()
        else:
            raise Exception("Penalty not set")
    return redirect("/home")
