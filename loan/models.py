from django.db import models
from users.models import Profile
from branch.models import Branch
from django.utils import timezone
from clientApp.models import Person

class LoanProduct(models.Model):
    name = models.CharField(max_length=255)
    interest = models.DecimalField(max_digits=5, decimal_places=2)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name + ' - ' + str(self.interest) + '%'

class SecurityType(models.Model):
    name = models.CharField(max_length=255)
    power = models.IntegerField(default=1)

    def __str__(self):
        return self.name
    
class Remarks(models.Model):
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE)
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.loan.branch.name + ' - ' + self.loan.loan_officer.user.fullname + ' - ' + self.remarks
    

class Loan(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    disbursment_branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="disbursment_branch")
    loan_officer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    client = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    requested_amount = models.IntegerField()
    unit_interest = models.IntegerField(null=True, blank=True)
    installment = models.IntegerField(null=True, blank=True)
    account_interest = models.IntegerField(null=True, blank=True)
    recommended_amount = models.IntegerField()
    given_amount = models.IntegerField(null=True, blank=True)
    demanded_amount = models.IntegerField(null=True, blank=True)
    loan_term = models.IntegerField()
    loan_term_type_of_period = models.CharField(max_length=20, default='months')
    payment_frequency = models.CharField(max_length=20, default='monthly')
    security_type = models.ForeignKey(SecurityType, on_delete=models.CASCADE, null=True, blank=True)
    security_description = models.CharField( max_length=255, null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    deposit_made_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_by")
    guarantor = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name="guarantor")
    guarantor_relationship = models.CharField(max_length=255, null=True, blank=True)
    status_choices = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('DISBURSED', 'Disbursed'),
        ('DEFAULTING', 'Defaulting'),
        ('CLOSED', 'Closed'),
        ('WRITTEN_OFF', 'Written Off'),

    ]
    status = models.CharField(max_length=20, choices=status_choices, default='PENDING')
    loan_product = models.ForeignKey(LoanProduct, on_delete=models.CASCADE)

    def __str__(self):
        return self.branch.name + ' - ' + self.loan_officer.user.fullname + ' - ' + str(self.given_amount) + ' - ' + str(self.loan_term) + ' - ' + str(self.interest_rate) + ' - ' + self.status

    def approve(self, approved_by):
        self.status = 'APPROVED'
        self.approved_at = timezone.now()
        self.approved_by = approved_by
        self.save()

    def reject(self, approved_by):
        self.status = 'REJECTED'
        self.approved_at = timezone.now()
        self.approved_by = approved_by
        self.save()
        
class Document(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    document = models.FileField(upload_to='loan_documents/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.loan.branch.name + ' - ' + self.loan.loan_officer.user.fullname + ' - ' + self.loan.status 
        

class LoanAmortization(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(null=True, blank=True)
    principal = models.IntegerField(null=True, blank=True)
    interest = models.IntegerField(null=True, blank=True)
    ending_balance = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.loan.branch.name + ' - ' + self.loan.loan_officer.user.fullname + ' - ' + self.loan.status + ' - ' + self.status
    



class LoanImage(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='loan_images/')

    def __str__(self):
        return self.loan.branch.name + ' - ' + self.loan.loan_officer.user.fullname + ' - ' + self.loan.status + ' - ' + self.security_type.name
    
class Deposit(models.Model):
    deposit = models.IntegerField(null=True, blank=True)
    previous_balance = models.IntegerField(null=True, blank=True)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    interest = models.IntegerField(null=True, blank=True)
    ammortization = models.ForeignKey(LoanAmortization, on_delete=models.CASCADE, null=True, blank=True)
    deposited_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
class Penalty(models.Model):
    percentage = models.IntegerField()  
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return (str(self.percentage)) + '%'
    