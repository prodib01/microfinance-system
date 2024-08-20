from django.contrib import admin
from .models import Loan, LoanProduct, SecurityType, Deposit, Document, LoanGuarantor, LoanImage, LoanAmortization, Payments, SystemParameters

admin.site.register(Loan)
admin.site.register(LoanProduct)
admin.site.register(SecurityType)
admin.site.register(Deposit)
admin.site.register(Document)
admin.site.register(LoanGuarantor)
admin.site.register(LoanImage)
admin.site.register(LoanAmortization)
admin.site.register(Payments)
admin.site.register(SystemParameters)
