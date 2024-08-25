from django.db import models
from users.models import MuroUser
from utilities.choices import (
    account_type_choices,
    transaction_type_choices,
    cash_flow_classification_choices,
    income_statement_classification_choices,
    account_group_choices,
)
from utilities.enums import (
    AccountType,
    TransactionType,
    CashFlowClassification,
    IncomeStatementClassification,
    AccountGroup,
)


class Account(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    group = models.CharField(
        max_length=255,
        choices=account_group_choices,
        default=AccountGroup.CURRENT_ASSETS.value,
    )
    description = models.TextField(null=True, blank=True)
    account_type = models.CharField(
        max_length=10, choices=account_type_choices, default=AccountType.ASSET.value
    )
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    title = models.CharField(max_length=255)
    cash_flow_classification = models.CharField(
        max_length=255,
        choices=cash_flow_classification_choices,
        default=CashFlowClassification.OPERATING_ACTIVITIES.value,
    )
    income_statement_classification = models.CharField(
        max_length=255,
        choices=income_statement_classification_choices,
        default=IncomeStatementClassification.REVENUE.value,
    )
    narration = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class JournalEntries(models.Model):
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, related_name="journal_entries"
    )
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="journal_entries"
    )
    entry_type = models.CharField(
        max_length=10,
        choices=transaction_type_choices,
        default=TransactionType.DEBIT.value,
    )
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    account_balance_before_transaction = models.DecimalField(
        max_digits=20, decimal_places=2
    )
    account_balance_after_transaction = models.DecimalField(
        max_digits=20, decimal_places=2
    )
    narration = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction} - {self.account} - {self.entry_type}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Journal Entries"
