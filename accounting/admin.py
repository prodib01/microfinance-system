from django.contrib import admin
from .models import Account, Transaction, JournalEntries


class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "account_type", "balance")
    list_filter = ("account_type",)
    search_fields = ("name", "code")
    list_per_page = 20


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "cash_flow_classification",
        "income_statement_classification",
    )
    list_filter = ("cash_flow_classification", "income_statement_classification")
    search_fields = ("title",)
    list_per_page = 20


class JournalEntriesAdmin(admin.ModelAdmin):
    list_display = ("transaction", "account", "amount", "entry_type")
    list_filter = ("entry_type",)
    search_fields = ("transaction", "account")
    list_per_page = 20


admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(JournalEntries, JournalEntriesAdmin)
