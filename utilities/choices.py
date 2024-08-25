payment_type_choices = [
    ("PENALTY", "PENALTY"),
    ("INTEREST", "INTEREST"),
    ("PRINCIPAL", "PRINCIPAL"),
]

status_choices = [
    ("PENDING", "Pending"),
    ("APPROVED", "Approved"),
    ("REJECTED", "Rejected"),
    ("DISBURSED", "Disbursed"),
    ("DEFAULTING", "Defaulting"),
    ("CLOSED", "Closed"),
    ("WRITTEN_OFF", "Written Off"),
]

account_type_choices = [
    ("ASSET", "Asset"),
    ("LIABILITY", "Liability"),
    ("EQUITY", "Equity"),
    ("REVENUE", "Revenue"),
    ("EXPENSE", "Expense"),
]

role_choices = [
    ("MURO_MANAGER", "Muro Manager"),
    ("BUSINESS_SUPERVISOR", "Business Supervisor"),
    ("RELATIONSHIP_OFFICER", "Relationship Officer"),
    ("LOAN_OFFICER", "Loan Officer"),
    ("ACCOUNTANT", "Accountant"),
    ("BRANCH_MANAGER", "Branch Manager"),
]

marital_status_choices = [
    ("S", "Single"),
    ("M", "Married"),
    ("D", "Divorced"),
    ("W", "Widowed"),
]
gender_choices = [
    ("M", "Male"),
    ("F", "Female"),
]

transaction_type_choices = [
    ("DEBIT", "Debit"),
    ("CREDIT", "Credit"),
]

cash_flow_classification_choices = [
    ("INVESTING_ACTIVITIES", "Investing Activities"),
    ("FINANCING_ACTIVITIES", "Financing Activities"),
    ("OPERATING_ACTIVITIES", "Operating Activities"),
]

income_statement_classification_choices = [
    ("REVENUE", "Revenue"),
    ("EXPENSE", "Expense"),
]

account_group_choices = [
    ("CURRENT_ASSETS", "Current Assets"),
    ("FIXED_ASSETS", "Fixed Assets"),
    ("CURRENT_LIABILITIES", "Current Liabilities"),
    ("LONG_TERM_LIABILITIES", "Long Term Liabilities"),
    ("EQUITY", "Equity"),
    ("REVENUE", "Revenue"),
    ("EXPENSE", "Expense"),
]
