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

type_choices = [
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
    ('S', 'Single'),
    ('M', 'Married'),
    ('D', 'Divorced'),
    ('W', 'Widowed'),
]
gender_choices = [
    ('M', 'Male'),
    ('F', 'Female'),
]