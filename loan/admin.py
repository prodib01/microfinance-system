from django.contrib import admin
from .models import Loan, LoanProduct, SecurityType, Deposit, Penalty, Document, LoanGuarantor, LoanImage

admin.site.register(Loan)
admin.site.register(LoanProduct)
admin.site.register(SecurityType)
admin.site.register(Deposit)
admin.site.register(Penalty)
admin.site.register(Document)
admin.site.register(LoanGuarantor)
admin.site.register(LoanImage)