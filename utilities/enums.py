from enum import Enum


class TransactionTitle(Enum):
    LOAN_DISBURSEMENT = "Loan Disbursement"
    LOAN_REPAYMENT = "Loan Repayment"


class TransactionType(Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


class AccountType(Enum):
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"
    EQUITY = "EQUITY"
    REVENUE = "REVENUE"
    EXPENSE = "EXPENSE"


class CashFlowClassification(Enum):
    INVESTING_ACTIVITIES = "INVESTING_ACTIVITIES"
    FINANCING_ACTIVITIES = "FINANCING_ACTIVITIES"
    OPERATING_ACTIVITIES = "OPERATING_ACTIVITIES"


class IncomeStatementClassification(Enum):
    REVENUE = "REVENUE"
    EXPENSE = "EXPENSE"
