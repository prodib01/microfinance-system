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
from loan.views import calculate_loans_demanded_amount, calculate_total_principal_balance, calculate_total_interest_balance
from utilities.enums import (
    CashFlowClassification,
    IncomeStatementClassification,
    TransactionTitle,
    TransactionType,
    UserRoles,
)
from utilities.helpers import (
    get_account,
    get_system_parameter,
    record_transaction,
    record_journal_entry,
)
from django.db import transaction as django_transaction


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
    print(request.user.profile.role)
    people = Person.objects.all()
    # all_loans_about_to_expire()
    loan_products = LoanProduct.objects.all()
    security_types = SecurityType.objects.all()

    if request.user.profile.role == UserRoles.RELATIONSHIP_OFFICER.value:
        active_loans = Loan.objects.filter(status="APPROVED").order_by("-approved_at")[
            :4
        ]
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
        notifications = Notification.objects.filter(is_read=False).order_by("-created_at")
        total_loans_approved = Loan.objects.filter(status="APPROVED")

    elif request.user.profile.role == UserRoles.LOAN_OFFICER.value:
        active_loans = Loan.objects.filter(
            loan_officer=request.user.profile, status="APPROVED"
        ).order_by("-approved_at")[:4]
        approved_loans = (
            Loan.objects.filter(
                status="APPROVED", loan_officer=request.user.profile
            ).count()
            or 0
        )
        total_amount_approved_loans = (
            Loan.objects.filter(
                status="APPROVED", loan_officer=request.user.profile
            ).aggregate(total_amount=models.Sum("given_amount"))["total_amount"]
            or 0
        )
        total_amount_given_today = (
            Loan.objects.filter(
                status="APPROVED",
                loan_officer=request.user.profile,
                approved_at=datetime.datetime.now().date(),
            ).aggregate(total_amount=models.Sum("given_amount"))["total_amount"]
            or 0
        )
        notifications = Notification.objects.filter(is_read=False, loan__loan_officer=request.user.profile).order_by("-created_at")
        total_loans_approved = Loan.objects.filter(status="APPROVED", loan_officer=request.user.profile)

    else:
        active_loans = Loan.objects.filter(
            disbursment_branch=request.user.profile.branch
        ).order_by("-approved_at")[:4]
        approved_loans = (
            Loan.objects.filter(
                status="APPROVED", disbursment_branch=request.user.profile.branch
            ).count()
            or 0
        )
        total_amount_approved_loans = (
            Loan.objects.filter(
                status="APPROVED", disbursment_branch=request.user.profile.branch
            ).aggregate(total_amount=models.Sum("given_amount"))["total_amount"]
            or 0
        )
        total_amount_given_today = (
            Loan.objects.filter(
                status="APPROVED",
                disbursment_branch=request.user.profile.branch,
                approved_at=datetime.datetime.now().date(),
            ).aggregate(total_amount=models.Sum("given_amount"))["total_amount"]
            or 0
        )
        notifications = Notification.objects.filter(is_read=False, loan__disbursment_branch=request.user.profile.branch).order_by("-created_at")
        total_loans_approved = Loan.objects.filter(status="APPROVED", disbursment_branch=request.user.profile.branch)
    total_amount_demanded = calculate_loans_demanded_amount(total_loans_approved)
    total_principal_balance = calculate_total_principal_balance(total_loans_approved)
    total_interest_balance = calculate_total_interest_balance(total_loans_approved)
    user_type = request.user.profile.role
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
        "total_amount_demanded": total_amount_demanded,
        "total_principal_balance": total_principal_balance,
        "total_interest_balance": total_interest_balance,
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

        loan_demanding_account = get_account("LOAN_DEMANDING_ACCOUNT")
        loan_receivables_account = get_account("LOAN_RECEIVABLES_ACCOUNT")
        with django_transaction.atomic():
            total_balance = amount_brought + Decimal(loan.client_loan_account_balance)
            deposit = Deposit.objects.create(
                loan=loan,
                amount_deposited=amount_brought,
                deposited_at=deposit_made_at,
                amount_found_on_account=loan.client_loan_account_balance,
                loan_balance_at_time_of_deposit=loan.demanded_amount,
            )
            deposit_made_at_dtime = datetime.datetime.strptime(
                deposit_made_at, "%Y-%m-%d"
            ).replace(tzinfo=datetime.timezone.utc)

            narration = f"Deposit of {amount_brought.__round__(2)} was made on {deposit_made_at}"
            transaction = record_transaction(
                title=TransactionTitle.LOAN_REPAYMENT.value,
                narration=narration,
                cash_flow_classification=CashFlowClassification.OPERATING_ACTIVITIES.value,
                income_statement_classification=IncomeStatementClassification.REVENUE.value,
            )
            loan_amortizations = LoanAmortization.objects.filter(loan=loan)
            penalty = get_system_parameter("PENALTY").int_value
            if penalty is not None:
                for loan_amortization in loan_amortizations:
                    if loan_amortization.payment_date < deposit_made_at_dtime:
                        if loan_amortization.status == "PENDING":
                            days_in_arreas = int(
                                (
                                    deposit_made_at_dtime
                                    - loan_amortization.penalty_date
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

                                if penalty_paid > 0:
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

                                    penalty_debit_account = get_account(
                                        "PENALTY_DEBIT_ACCOUNT"
                                    )
                                    penalty_credit_account = get_account(
                                        "PENALTY_CREDIT_ACCOUNT"
                                    )
                                    narration = f"Penalty of {penalty_paid.__round__(2)} was paid for {days_in_arreas} days of arrears"
                                    record_journal_entry(
                                        transaction=transaction,
                                        account=penalty_debit_account,
                                        amount=penalty_paid,
                                        entry_type=TransactionType.DEBIT.value,
                                        narration=narration,
                                    )
                                    record_journal_entry(
                                        transaction=transaction,
                                        account=penalty_credit_account,
                                        amount=penalty_paid,
                                        entry_type=TransactionType.CREDIT.value,
                                        narration=narration,
                                    )

                            if total_balance > 0:
                                if loan_amortization.interest_balance > 0:
                                    if (
                                        total_balance
                                        < loan_amortization.interest_balance
                                    ):
                                        interest_paid = total_balance
                                    else:
                                        interest_paid = (
                                            loan_amortization.interest_balance
                                        )
                                    total_balance -= interest_paid
                                    loan.demanded_amount -= Decimal(interest_paid)
                                    old_interest_balance = (
                                        loan_amortization.interest_balance
                                    )
                                    new_interest_balance = (
                                        old_interest_balance - Decimal(interest_paid)
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
                                    record_journal_entry(
                                        transaction=transaction,
                                        account=loan_demanding_account,
                                        amount=interest_paid,
                                        entry_type=TransactionType.DEBIT.value,
                                        narration=narration,
                                    )
                                    record_journal_entry(
                                        transaction=transaction,
                                        account=loan_receivables_account,
                                        amount=interest_paid,
                                        entry_type=TransactionType.CREDIT.value,
                                        narration=narration,
                                    )

                            if total_balance > 0:
                                if total_balance < loan_amortization.principal_balance:
                                    principal_paid = total_balance
                                elif (
                                    total_balance >= loan_amortization.principal_balance
                                ):
                                    principal_paid = loan_amortization.principal_balance

                                total_balance -= principal_paid
                                loan.demanded_amount -= Decimal(principal_paid)
                                old_principal_balance = (
                                    loan_amortization.principal_balance
                                )
                                new_principal_balance = old_principal_balance - Decimal(
                                    principal_paid
                                )
                                narration = f"Principal of {principal_paid.__round__(2)} was paid of the total balance of {old_principal_balance} making the new balance {new_principal_balance.__round__(2)}"
                                loan_amortization.principal_balance = (
                                    new_principal_balance
                                )
                                Payments.objects.create(
                                    amount=principal_paid,
                                    payment_date=deposit_made_at,
                                    ammortization=loan_amortization,
                                    payment_type="PRINCIPAL",
                                    deposit=deposit,
                                    narration=narration,
                                )
                                record_journal_entry(
                                    transaction=transaction,
                                    account=loan_demanding_account,
                                    amount=principal_paid,
                                    entry_type=TransactionType.DEBIT.value,
                                    narration=narration,
                                )
                                record_journal_entry(
                                    transaction=transaction,
                                    account=loan_receivables_account,
                                    amount=principal_paid,
                                    entry_type=TransactionType.CREDIT.value,
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
                deposit.loan_balance_after_deposit = loan.demanded_amount
                deposit.save()
            else:
                raise Exception("Penalty not set")
    return redirect("/home")


def calculate_demanded_penalty(loan: Loan) -> float:
    pass

