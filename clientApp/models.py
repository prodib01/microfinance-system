from django.db import models

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


class Person(models.Model):
    full_name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    nin = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True, null=True, blank=True, default=None)
    account_balance = models.FloatField(default=0, null=True, blank=True)
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=15, choices=gender_choices, default='M')
    dob = models.DateField(null=True, blank=True, default=None)
    business = models.CharField(max_length=100, null=True, blank=True, default=None)
    address = models.CharField(max_length=200)
    number_of_children = models.IntegerField(default=0, null=True, blank=True)
    marital_status = models.CharField(max_length=15, default='S')
    spouse_name = models.CharField(max_length=100, null=True, blank=True, default=None)
    spouse_phone = models.CharField(max_length=15, null=True, blank=True, default=None)
    client_code = models.CharField(max_length=20, null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Clients'

