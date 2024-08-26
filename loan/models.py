from django.db import models
from users.models import MuroUser, Profile
from branch.models import Branch
from django.utils import timezone
from clientApp.models import Person
from utilities.choices import payment_type_choices, status_choices


class LoanProduct(models.Model):
    name = models.CharField(max_length=255)
    interest = models.DecimalField(max_digits=5, decimal_places=2)
    code = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SecurityType(models.Model):
    name = models.CharField(max_length=255)
    power = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Loan(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    disbursment_branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="disbursment_branch",
    )
    loan_officer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    client = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    requested_amount = models.IntegerField()
    unit_interest = models.IntegerField(null=True, blank=True)
    installment = models.IntegerField(null=True, blank=True)
    account_interest = models.IntegerField(null=True, blank=True)
    recommended_amount = models.IntegerField()
    given_amount = models.IntegerField(null=True, blank=True)
    demanded_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    loan_term = models.IntegerField()
    loan_term_type_of_period = models.CharField(max_length=20, default="months")
    payment_frequency = models.CharField(max_length=20, default="monthly")
    security_type = models.ForeignKey(
        SecurityType, on_delete=models.CASCADE, null=True, blank=True
    )
    security_description = models.CharField(max_length=255, null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    deposit_made_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_by",
    )
    status = models.CharField(max_length=20, choices=status_choices, default="PENDING")
    loan_product = models.ForeignKey(LoanProduct, on_delete=models.CASCADE)
    client_loan_account_balance = models.DecimalField(
        default=0, max_digits=10, decimal_places=2
    )

    def __str__(self):
        return (
                self.branch.name
                + " - "
                + self.loan_officer.user.fullname
                + " - "
                + str(self.given_amount)
                + " - "
                + str(self.loan_term)
                + " - "
                + str(self.interest_rate)
                + " - "
                + self.status
        )

    def approve(self, approved_by):
        self.status = "APPROVED"
        self.approved_at = timezone.now()
        self.approved_by = approved_by
        self.save()

    def reject(self, approved_by):
        self.status = "REJECTED"
        self.approved_at = timezone.now()
        self.approved_by = approved_by
        self.save()


class Remarks(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return (
                self.loan.branch.name
                + " - "
                + self.loan.loan_officer.user.fullname
                + " - "
                + self.remarks
        )


class LoanGuarantor(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    guarantor = models.ForeignKey(Person, on_delete=models.CASCADE)
    guarantee = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="guarantee"
    )
    relationship = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
                self.guarantor.full_name
                + " -"
                + self.guarantee.full_name
                + " -"
                + str(self.loan)
        )


class Document(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    document = models.FileField(upload_to="loan_documents/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
                self.loan.branch.name
                + " - "
                + self.loan.loan_officer.user.fullname
                + " - "
                + self.loan.status
        )


class LoanAmortization(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(null=True, blank=True)
    penalty_date = models.DateTimeField(null=True, blank=True)
    principal = models.IntegerField(null=True, blank=True)
    principal_balance = models.IntegerField(null=True, blank=True)
    interest = models.IntegerField(null=True, blank=True)
    interest_balance = models.IntegerField(null=True, blank=True)
    ending_balance = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
                self.loan.branch.name
                + " - "
                + self.loan.loan_officer.user.fullname
                + " - "
                + self.loan.status
                + " - "
                + self.status
        )


class LoanImage(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="loan_images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
                self.loan.branch.name
                + " - "
                + self.loan.loan_officer.user.fullname
                + " - "
                + self.loan.status
        )


class Deposit(models.Model):
    amount_deposited = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=2
    )
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    deposited_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    amount_found_on_account = models.DecimalField(
        default=0, max_digits=10, decimal_places=2
    )
    received_by = models.ForeignKey(
        MuroUser, on_delete=models.PROTECT, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return (
                self.loan.branch.name
                + " - "
                + self.loan.loan_officer.user.fullname
                + " - "
                + self.loan.status
        )


class Payments(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    narration = models.TextField(null=True, blank=True)
    payment_date = models.DateTimeField()
    ammortization = models.ForeignKey(
        LoanAmortization, on_delete=models.CASCADE, null=True, blank=True
    )
    payment_type = models.CharField(
        max_length=20, choices=payment_type_choices, default="INTEREST"
    )
    deposit = models.ForeignKey(
        Deposit, on_delete=models.CASCADE, null=True, blank=True, related_name="payments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
                self.payment_type
                + " - "
                + str(self.amount)
                + " - "
                + str(self.payment_date)
        )


class SystemParameters(models.Model):
    code = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    string_value = models.CharField(max_length=255, null=True, blank=True)
    int_value = models.IntegerField(null=True, blank=True)
    decimal_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    bool_value = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super(SystemParameters, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "System Parameters"
        ordering = ["code"]
