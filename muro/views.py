from datetime import datetime
import io
from django.shortcuts import render
from loan.models import Loan, LoanAmortization
from django.utils.dateparse import parse_date
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.utils import timezone
from accounting.models import Account
from loan.views import (
    calculate_total_interest_balance,
    calculate_total_principal_balance,
)
from utilities.enums import AccountGroup, UserRoles
from django.db.models import Q


def index(request):
    return render(request, "index.html")


def loans(request):
    if request.user.profile.role == UserRoles.RELATIONSHIP_OFFICER.value:
        loans = Loan.objects.all()
    elif request.user.profile.role == UserRoles.LOAN_OFFICER.value:
        loans = Loan.objects.filter(loan_officer=request.user.profile)
    else:
        # disbursment_branch or branch
        loans = Loan.objects.filter(
            Q(branch=request.user.profile.branch)
            | Q(disbursment_branch=request.user.profile.branch)
        )
    return render(request, "pages/loans.html", {"active": "loans", "loans": loans})


def search_loan(request):
    if request.method == "POST":
        search = request.POST["search"]
        loans = Loan.objects.filter(client__full_name__icontains=search)
        return render(request, "pages/loans.html", {"active": "loans", "loans": loans})
    else:
        return render(request, "pages/loans.html", {"active": "loans", "loans": loans})


def financialstatements(request):
    all_accounts = Account.objects.all().order_by("name")
    current_assets = Account.objects.filter(group=AccountGroup.CURRENT_ASSETS.value)
    sum_current_assets = sum([account.balance for account in current_assets])
    fixed_assets = Account.objects.filter(group=AccountGroup.FIXED_ASSETS.value)
    sum_fixed_assets = sum([account.balance for account in fixed_assets])
    current_liabilities = Account.objects.filter(
        group=AccountGroup.CURRENT_LIABILITIES.value
    )
    sum_current_liabilities = sum([account.balance for account in current_liabilities])
    long_term_liabilities = Account.objects.filter(
        group=AccountGroup.LONG_TERM_LIABILITIES.value
    )
    sum_long_term_liabilities = sum(
        [account.balance for account in long_term_liabilities]
    )
    equity = Account.objects.filter(group=AccountGroup.EQUITY.value)
    sum_equity = sum([account.balance for account in equity])
    total_assets = sum_fixed_assets + sum_current_assets
    total_liabilities = sum_current_liabilities + sum_long_term_liabilities
    total_equity_and_liabilities = sum_equity + total_liabilities

    return render(
        request,
        "pages/financialstatements.html",
        {
            "active": "financialstatements",
            "accounts": all_accounts,
            "current_assets": current_assets,
            "sum_current_assets": sum_current_assets,
            "fixed_assets": fixed_assets,
            "sum_fixed_assets": sum_fixed_assets,
            "current_liabilities": current_liabilities,
            "sum_current_liabilities": sum_current_liabilities,
            "long_term_liabilities": long_term_liabilities,
            "sum_long_term_liabilities": sum_long_term_liabilities,
            "equity": equity,
            "sum_equity": sum_equity,
            "total_assets": total_assets,
            "total_liabilities": total_liabilities,
            "total_equity_and_liabilities": total_equity_and_liabilities,
        },
    )


def reports(request):
    if request.user.profile.role == UserRoles.RELATIONSHIP_OFFICER.value:
        loans = Loan.objects.filter(status="APPROVED")
    elif request.user.profile.role == UserRoles.LOAN_OFFICER.value:
        loans = Loan.objects.filter(
            loan_officer=request.user.profile, status="APPROVED"
        )
    else:
        loans = Loan.objects.filter(
            Q(branch=request.user.profile.branch)
            | Q(disbursment_branch=request.user.profile.branch)
        ).filter(status="APPROVED")
    for loan in loans:
        actual_loan = loans.filter(id=loan.id)
        loan.interest_balance = calculate_total_interest_balance(actual_loan)
        loan.principal_balance = calculate_total_principal_balance(actual_loan)

    loans = loans.order_by("-demanded_amount")
    context = {
        "loans": loans,
    }
    return render(request, "pages/reports.html", context)


def download_loans_pdf(request):
    selected_month = request.GET.get("month")
    selected_year = request.GET.get("year")

    loans = Loan.objects.all()
    if selected_month and selected_year:
        loans = loans.filter(
            created_at__year=int(selected_year), created_at__month=int(selected_month)
        )

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 72
    header_height = 40  # Increased height for better spacing
    row_height = 20
    y = height - margin - header_height

    column_widths = {
        "branch": 80,
        "loan_officer": 55,
        "client": 100,
        "amount": 60,
        "date": 80,
        "status": 73,
        "payment_date": 95,
        "amount_paid": 60,
    }

    column_positions = {}
    current_position = margin
    for column, width in column_widths.items():
        column_positions[column] = current_position
        current_position += width

    def add_header():
        p.setFont("Helvetica-Bold", 12)
        y = height - margin - header_height
        p.drawString(column_positions["branch"], y, "Branch")
        p.drawString(column_positions["loan_officer"], y, "Officer")
        p.drawString(column_positions["client"], y, "Client")
        p.drawString(column_positions["amount"], y, "Amount")
        p.drawString(column_positions["date"], y, "Created At")
        p.drawString(column_positions["status"], y, "Status")
        p.drawString(column_positions["payment_date"], y, "Payment Date")
        p.drawString(column_positions["amount_paid"], y, "Paid")

    def add_row(loan):
        nonlocal y
        if y < margin + header_height:
            p.showPage()
            y = height - margin - header_height
            add_header()
        p.setFont("Helvetica", 10)
        y -= row_height
        p.drawString(column_positions["branch"], y, loan.branch.name)
        p.drawString(
            column_positions["loan_officer"], y, loan.loan_officer.user.fullname
        )
        p.drawString(
            column_positions["client"], y, loan.client.full_name if loan.client else ""
        )
        p.drawString(column_positions["amount"], y, str(loan.requested_amount))
        p.drawString(column_positions["date"], y, loan.created_at.strftime("%Y-%m-%d"))
        p.drawString(column_positions["status"], y, loan.status)

        # Add LoanAmortization details if available
        amortizations = LoanAmortization.objects.filter(loan=loan)
        for amortization in amortizations:
            y -= row_height
            p.drawString(
                column_positions["payment_date"],
                y,
                (
                    amortization.payment_date.strftime("%Y-%m-%d")
                    if amortization.payment_date
                    else ""
                ),
            )
            p.drawString(
                column_positions["amount_paid"],
                y,
                str(amortization.amount_paid) if amortization.amount_paid else "",
            )

    p.setFont("Helvetica-Bold", 16)
    p.drawString(margin, height - margin + 20, "Loans Report")
    add_header()

    for loan in loans:
        add_row(loan)

    p.showPage()
    p.save()

    buffer.seek(0)
    response = FileResponse(buffer, as_attachment=True, filename="loans_report.pdf")
    return response


def test(request):
    return render(request, "pages/test.html")


def sec_page(request):
    return render(request, "pages/secPage.html")
