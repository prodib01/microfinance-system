import io
from django.shortcuts import render 
from loan.models import Loan,LoanAmortization
from django.utils.dateparse import parse_date
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.utils import timezone
  
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

def financialstatements(request):
    rejected_loans = Loan.objects.filter(status='REJECTED').count()
    approved_loans = Loan.objects.filter(status='APPROVED').count()
    pending_loans = Loan.objects.filter(status='PENDING').count()
    return render(request, 'pages/financialstatements.html', {'active': 'financialstatements', 'loan_count':[]})

from datetime import datetime

def reports(request):
    # Get the current date
    now = timezone.now()
    current_month = now.month
    current_year = now.year

    # Fetch the selected month and year from the request
    selected_month = request.GET.get('month', current_month)
    selected_year = request.GET.get('year', current_year)

    # Fetch loans based on the selected month and year
    loans = Loan.objects.filter(
        created_at__year=selected_year,
        created_at__month=selected_month
    )

    # Generate a range of years for the year select dropdown
    year_range = range(current_year - 10, current_year + 1)

    context = {
        'loans': loans,
        'year_range': year_range,
        'selected_month': selected_month,
        'selected_year': selected_year
    }
    return render(request, 'pages/reports.html', context)


def download_loans_pdf(request):
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')

    loans = Loan.objects.all()
    if selected_month and selected_year:
        loans = loans.filter(
            created_at__year=int(selected_year),
            created_at__month=int(selected_month)
        )

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 72
    header_height = 40  # Increased height for better spacing
    row_height = 20
    y = height - margin - header_height

    column_widths = {
        'branch': 80,
        'loan_officer': 55,
        'client': 60,
        'amount': 60,
        'date': 80,
        'status': 73,
        'payment_date': 95,
        'amount_paid': 60
    }

    column_positions = {}
    current_position = margin
    for column, width in column_widths.items():
        column_positions[column] = current_position
        current_position += width

    def add_header():
        p.setFont("Helvetica-Bold", 12)
        y = height - margin - header_height
        p.drawString(column_positions['branch'], y, "Branch")
        p.drawString(column_positions['loan_officer'], y, "Officer")
        p.drawString(column_positions['client'], y, "Client")
        p.drawString(column_positions['amount'], y, "Amount")
        p.drawString(column_positions['date'], y, "Created At")
        p.drawString(column_positions['status'], y, "Status")
        p.drawString(column_positions['payment_date'], y, "Payment Date")
        p.drawString(column_positions['amount_paid'], y, "Paid")

    def add_row(loan):
        nonlocal y
        if y < margin + header_height:
            p.showPage()
            y = height - margin - header_height
            add_header()
        p.setFont("Helvetica", 10)
        y -= row_height
        p.drawString(column_positions['branch'], y, loan.branch.name)
        p.drawString(column_positions['loan_officer'], y, loan.loan_officer.user.fullname)
        p.drawString(column_positions['client'], y, loan.client.full_name if loan.client else '')
        p.drawString(column_positions['amount'], y, str(loan.requested_amount))
        p.drawString(column_positions['date'], y, loan.created_at.strftime('%Y-%m-%d'))
        p.drawString(column_positions['status'], y, loan.status)

        # Add LoanAmortization details if available
        amortizations = LoanAmortization.objects.filter(loan=loan)
        for amortization in amortizations:
            y -= row_height
            p.drawString(column_positions['payment_date'], y, amortization.payment_date.strftime('%Y-%m-%d') if amortization.payment_date else '')
            p.drawString(column_positions['amount_paid'], y, str(amortization.amount_paid) if amortization.amount_paid else '')

    p.setFont("Helvetica-Bold", 16)
    p.drawString(margin, height - margin + 20, "Loans Report")
    add_header()

    for loan in loans:
        add_row(loan)

    p.showPage()
    p.save()

    buffer.seek(0)
    response = FileResponse(buffer, as_attachment=True, filename='loans_report.pdf')
    return response



def test(request):
    return render(request, 'pages/test.html')

def sec_page(request):
    return render(request, 'pages/secPage.html')    