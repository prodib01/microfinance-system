from accounting.models import Account, Transaction, JournalEntries
from loan.models import SystemParameters
from utilities.enums import (
    CashFlowClassification,
    IncomeStatementClassification,
    TransactionType,
)

accounts_increased_by_debits = [
    "ASSET",
    "EXPENSE",
]

accounts_increased_by_credits = [
    "LIABILITY",
    "EQUITY",
    "REVENUE",
]


def get_system_parameter(name):
    return SystemParameters.objects.get(name=name)


def record_transaction(
    title,
    description,
    cash_flow_classification=CashFlowClassification.OPERATING_ACTIVITIES.value,
    income_statement_classification=IncomeStatementClassification.REVENUE.value,
):
    return Transaction.objects.create(
        title=title,
        description=description,
        cash_flow_classification=cash_flow_classification,
        income_statement_classification=income_statement_classification,
    )


def record_journal_entry(
    transaction, account, amount, entry_type=TransactionType.DEBIT.value
):
    account_balance_before = account.balance
    account_balance_after = account_balance_before
    if account.account_type in accounts_increased_by_debits:
        if entry_type == TransactionType.DEBIT.value:
            account_balance_after += amount
        else:
            account_balance_after -= amount
    else:
        if entry_type == TransactionType.DEBIT.value:
            account_balance_after -= amount
        else:
            account_balance_after += amount
    account.balance = account_balance_after
    account.save()
    return JournalEntries.objects.create(
        transaction=transaction,
        account=account,
        amount=amount,
        entry_type=entry_type,
        account_balance_before=account_balance_before,
        account_balance_after=account_balance_after,
    )


def get_account(account_name):
    account_name = get_system_parameter(account_name).string_value
    return Account.objects.get(name=account_name)
