from django.contrib import admin
from .models import (
    Loan,
    LoanProduct,
    SecurityType,
    Deposit,
    LoanAmortization,
    Payments,
    SystemParameters,
)

# admin.site.register(Loan)
# admin.site.register(LoanProduct)
# admin.site.register(SecurityType)
# admin.site.register(Deposit)
# admin.site.register(Document)
# admin.site.register(LoanGuarantor)
# admin.site.register(LoanImage)
# admin.site.register(LoanAmortization)
# admin.site.register(Payments)
# admin.site.register(SystemParameters)


class LoanAdmin(admin.ModelAdmin):
    list_display = (
        "loan_product",
        "client",
        "branch",
        "loan_officer",
        "given_amount",
        "demanded_amount",
        "client_loan_account_balance",
        "account_interest",
        "unit_interest",
        "status",
        "approved_at",
    )
    list_filter = ("status", "branch", "loan_officer", "loan_product")
    search_fields = ("client", "branch", "loan_officer", "loan_product")
    list_per_page = 20


class LoanProductAdmin(admin.ModelAdmin):
    list_display = ("name", "interest", "code", "created_at")
    list_filter = ("name", "interest", "code")
    search_fields = ("name", "interest", "code")
    list_per_page = 20


class SecurityTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "power", "created_at")
    list_filter = ("name", "power")
    search_fields = ("name", "power")
    list_per_page = 20


class DepositAdmin(admin.ModelAdmin):
    list_display = (
        "loan",
        "amount_deposited",
        "amount_found_on_account",
        "deposited_at",
    )
    list_filter = ("loan", "deposited_at")
    search_fields = ("loan", "deposited_at")
    list_per_page = 20


class LoanAmortizationAdmin(admin.ModelAdmin):
    list_display = (
        "loan",
        "payment_date",
        "principal",
        "principal_balance",
        "interest",
        "interest_balance",
        "ending_balance",
        "status",
        "created_at",
    )
    list_filter = ("loan", "payment_date", "status")
    search_fields = ("loan", "payment_date", "status")
    list_per_page = 20


class PaymentsAdmin(admin.ModelAdmin):
    list_display = (
        "deposit",
        "ammortization",
        "amount",
        "payment_type",
        "narration",
        "payment_date",
    )
    list_filter = ("deposit", "ammortization", "payment_date")
    search_fields = ("deposit", "ammortization", "payment_type")
    list_per_page = 20


class SystemParametersAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "string_value",
        "int_value",
        "decimal_value",
        "bool_value",
        "created_at",
    )
    list_filter = ("name", "description", "created_at")
    search_fields = ("name", "description", "created_at")


admin.site.register(Loan, LoanAdmin)
admin.site.register(LoanProduct, LoanProductAdmin)
admin.site.register(SecurityType, SecurityTypeAdmin)
admin.site.register(Deposit, DepositAdmin)
admin.site.register(LoanAmortization, LoanAmortizationAdmin)
admin.site.register(Payments, PaymentsAdmin)
admin.site.register(SystemParameters, SystemParametersAdmin)
